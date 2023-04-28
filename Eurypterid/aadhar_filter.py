import cv2
import pytesseract
import re

data = dict()

img = cv2.imread("adhar1.jpg") # Enter the file path here 
blur = cv2.GaussianBlur(img, (3,3), 0)
gray_blur = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
text = pytesseract.image_to_string(thresh, lang='eng+tam+hin+tel+mal')

if 'male' in text.lower():
    data['gender']= 'MALE'
elif 'female' in text.lower():
    data['gender'] = 'FEMALE'

lines = text.split('\n')
lines = list(filter(None, lines))
alphanumeric_pattern = re.compile("[A-Za-z0-9 ]+")
valid_lines = []
print(lines)
for line in lines:
    if alphanumeric_pattern.fullmatch(line) is not None:
        valid_lines.append(line)
if len(valid_lines) >= 2:
    data['name'] = valid_lines[0]
    data['aadhar_no'] = valid_lines[1]
data['dob'] = re.findall(r'[0-9]{2}-[0-9]{2}-[0-9]{4}', text)
data['dob'] = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', text)
print(data)
