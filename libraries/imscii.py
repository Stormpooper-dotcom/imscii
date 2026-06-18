from PIL import Image

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