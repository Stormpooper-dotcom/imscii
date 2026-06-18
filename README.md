### IMSCII v2
A Flask web server that converts images into grayscale ASCII art.

### Features
- Grayscale Conversion: Maps image pixel brightness to text characters.
- Web Preview: Displays the ASCII output directly in the browser.
- Adjustable Width: Allows configuration of the output text width.
- Text Export: Saves the final ASCII art as a .txt file.

### Prerequisites
- Python 3.8
- pip

### Dependencies
- Flask: Handles server routing and requests.
- Pillow: Manages image resizing and pixel processing.
See requirements.txt for details.

### Configuration
Modify these variables to change behavior:
- chars (libraries/imscii.py): The character set used for brightness mapping.
- CLEANUP_SECS (app.py): The time before .txt files are auto cleaned up (give 10 secs extra for cleanup function)

### Download
1. Download zip file from releases
2. Extract
3. Open Powershell/Terminal
4. Run these commands:
   Windows
   ```Windows Powershell
   cd path/to/extracted/folder
   python -m venv venv
   venv/Scripts/activate
   pip install -r requirements.txt
   ```

   Linux
   ```Linux Terminal
   cd path/to/extracted/folder
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

### Usage
1. Open terminal, activate environment
2. Run `python app.py`
3. Type `localhost` into your browser address bar
4. Select file, width and if the ascii string is reversed
5. Click Convert

### License
This project is licensed under the MIT License - see the LICENSE file for details.

Happy ASCII-fying :)
