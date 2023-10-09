        
import os
import cv2
import pytesseract
from PIL import Image

# Path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory containing images
img_dir = r'C:\Users\jacki\Personal\Photos\photo_joe'
# Python-specific keywords you expect to find in images
keywords = ['import', 'def', 'class', 'for', 'while', 'if']

def is_taken_by_iphone(image_path):
    try:
        with Image.open(image_path) as image:
            exif_data = image._getexif()
            if exif_data:
                # 271 is the tag for 'Make' in EXIF data
                make = exif_data.get(271, '').upper()
                return 'IPHONE' in make
    except IOError:
        print(f"IOError: Unable to open or identify image file '{image_path}'.")
    except Exception as e:
        print(f"Error processing EXIF data for image: {image_path}, Error: {e}")
    return False


def contains_python_code(image_path):
    # if not is_taken_by_iphone(image_path):
    #     return False

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error loading image: {image_path}")
        return False
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    text = pytesseract.image_to_string(gray)

    # Check for Python-specific keywords
    for keyword in keywords:
        if keyword in text:
            print(f"Possible Python code found in image: {image_path}")
            with open(output_file_path, 'a') as output_file:
                output_file.write(image_path + '\n')
            return True
    return False

# Initialize the file for writing
output_file_path = r'C:\Users\jacki\Downloads\Homelab\recovered_code_Eric\possible python code photo names.txt'
with open(output_file_path, 'w') as f:  # Clear the file contents
    pass

for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, file)
            contains_python_code(image_path)
