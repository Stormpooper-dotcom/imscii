from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image
import time, uuid, os, threading


# GLOBALS
app = Flask(__name__)
jobs = {}
UPLOAD_FOLDER = "ascii_files"
CLEANUP_SECS = 60
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# IMSCII CODE
chars = " .:-=+*#%@"

def resize_image(image, new_width=80):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55) # 0.55 fixes font aspect ratio
    return image.resize((new_width, new_height))

def pixels_to_ascii(image, charset):
    pixels = image.getdata()
    return "".join([chars[pixel * len(chars) // 256] for pixel in pixels])

def img_to_ascii(path, width=80, reversed=False):
    local_chars = chars
    with Image.open(path) as image:
        image = image.convert("L") # to grayscale
        image = resize_image(image, width)

        if reversed:
            local_chars = local_chars[::-1]

        ascii_str = pixels_to_ascii(image, local_chars)

        # Split into lines
        img_width = image.width
        ascii_lines = [ascii_str[i:i+img_width] for i in range(0, len(ascii_str), img_width)]
        return "\n".join(ascii_lines)
    

# THREADING
def worker():
    print("[Worker] Running...")
    while True:
        for order_id, job in list(jobs.items()):
            if job["status"] == "queued":
                print(f"[Worker] Processing order {order_id}")

                job["status"] == "processing"

                ascii_art = img_to_ascii(job["filepath"], job["width"], job["reversed"])

                filename = f"{order_id}.txt"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                with open(filepath, "w") as f:
                    f.write(ascii_art)
                
                job["status"] = "done"
                job["result"] = ascii_art
                job["filename"] = filename

                os.remove(job["filepath"])

                time.sleep(0.2)

def cleanup():
    print("[Cleanup] Running...")
    while True:
        now = time.time()
        for order_id in list(jobs.keys()):
            job = jobs[order_id]
            if job.get("status") == "done":
                job_age = now - job.get("created_at", now)
                if job_age > 60:
                    filename = job.get("filename")
                    if filename:
                        filepath = os.path.join(UPLOAD_FOLDER, filename)
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                            except:
                                pass
                    del jobs[order_id]
                    print(f"[Cleanup] Deleted old job {order_id}")
        time.sleep(10)

def setup():
    print("[Setup] Deleting old files...")
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            os.remove(filepath)
            print(f"[Setup] Deleted old file {filename}")
        except Exception as e:
            print(f"[Setup] Could not delete old file {filename}: {e}")
    print("[Setup] Done!")


# ROUTES    
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/order", methods=["POST"])
def create_order():
    order_id = str(uuid.uuid4())[:6]

    file = request.files["image"]

    filename = f"{order_id}_upload.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    jobs[order_id] = {
        "status": "queued",
        "result": None,
        "filename": None,
        "width": int(request.form["width"]),
        "reversed": "reversed" in request.form,
        "filepath": filepath,
        "created_at": time.time()
    }
    print(f"Added job {order_id}")
    position = len([j for j in jobs.values() if j["status"] == "queued"])
    return render_template('waiting.html', order_id=order_id, position=position)

@app.route("/status/<order_id>")
def status(order_id):
    job = jobs.get(order_id)
    if not job:
        return jsonify({"error": "Order not found"}), 404
    
    queued_jobs = [j for j in jobs.values() if j["status"] == "queued"]
    position = len(queued_jobs)

    return jsonify({
        "status": job["status"],
        "position": position,
        "ascii": job.get("result"),
        "filename": job.get("filename")

    })

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)


# MAIN
if __name__ == "__main__":
    setup()
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=cleanup, daemon=True).start()
    app.run(host="0.0.0.0", port=80, threaded=True, debug=True)