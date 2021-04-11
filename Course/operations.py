import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def read_image(image):
    pil_image = Image.open(image)
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = get_grayscale(img)
    extractedInformation = pytesseract.image_to_string(gray)
    print(extractedInformation)
    return extractedInformation
