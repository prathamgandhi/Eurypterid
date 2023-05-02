from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from .forms import AadharUploadForm
from .forms import GateUploadForm

from .models import GateCandidate

import cv2
import pytesseract
import re

from collections import defaultdict

def aadhar_upload(request):
    if request.method == 'POST':
        if "file" in request.POST:
            print("hello")
            with open("tmp", "wb+") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            data = defaultdict(lambda: "")
            img = cv2.imread("tmp") # Enter the file path here 
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
            for line in lines:
                if alphanumeric_pattern.fullmatch(line) is not None:
                    valid_lines.append(line)
            if len(valid_lines) >= 2:
                data['name'] = valid_lines[0]
                data['aadhar_no'] = valid_lines[1]
            data['dob'] = re.findall(r'[0-9]{2}-[0-9]{2}-[0-9]{4}', text)
            data['dob'] = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', text)
            form = AadharUploadForm(initial={'name' : data['name'], 'dob' : data['dob'][0], 'aadhar_no' : data['aadhar_no'], 'gender' : data['gender']})
            return render(request, 'aadhar_details.html', {'form' : form})
        elif "details" in request.POST:

           return HttpResponse("Success")
    else:
        form = AadharUploadForm()
    return render(request, 'aadhar_details.html', {'form': form})


def gate_upload(request):
    if request.method == 'POST':
        if 'file' in request.POST:
            form = GateUploadForm(request.POST, request.FILES)
            form.fields['name'] = "Gandhi"
        elif 'details' in request.POST:
            if form.is_valid():
                name = form.cleaned_data['name']
                parent_name = form.cleaned_data['parent_name']
                reg_no = form.cleaned_data['reg_no']
                gate_score = form.cleaned_data['gate_score']
                air = form.cleaned_data['air']
                marks = form.cleaned_data['marks']
                instance = GateCandidate(name=name, parent_name=parent_name, reg_no=reg_no, gate_score=gate_score, air=air, marks=marks)
                instance.save()
                return HttpResponse("Success")
    else:
        form = GateUploadForm()
    print(form.__dict__)
    return render(request, 'gate_details.html', {'form' : form})