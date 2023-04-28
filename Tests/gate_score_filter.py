import cv2
import pytesseract
import re

data = dict()

img = cv2.imread("gatescore.png") # Enter the file path here 
text = pytesseract.image_to_string(img, lang='eng')
print(text)

