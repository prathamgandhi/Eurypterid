from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from .forms import AadharUploadForm
from .forms import GateUploadForm

from .models import GateCandidate
from .models import AadharCandidate

import cv2
import pytesseract
import re

import datetime
from collections import defaultdict

def aadhar_upload(request):
    if request.method == 'POST':
        if "file_upload" in request.POST:
            with open("tmp", "wb+") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            data = defaultdict(lambda: "")
            img = cv2.imread("tmp") # Enter the file path here 
            blur = cv2.GaussianBlur(img, (3,3), 0)
            gray_blur = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(thresh, lang='eng+tam+hin+tel+mal')
            print(text)
            if 'male' in text.lower():
                data['gender']= 'MALE'
            elif 'female' in text.lower():
                data['gender'] = 'FEMALE'

            data['dob'] = re.findall(r'[0-9]{2}-[0-9]{2}-[0-9]{4}', text)
            datetime_str = ""
            if len(data['dob']) > 0:
                format = "%d-%m-%Y"
            else:
                data['dob'] = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', text)
                format = "%d/%m/%Y"
            if len(data['dob']) > 0:
                datetime_str = datetime.datetime.strptime(data['dob'][0], format).date()

            lines = text.split('\n')
            space_rex = re.compile("[ ]*")
            space_removed_lines = []
            for line in lines:
                if space_rex.fullmatch(line) is None:
                    space_removed_lines.append(line)
            alphanumeric_pattern = re.compile("[A-Za-z0-9 ]+")
            valid_lines_temp = []
            for line in space_removed_lines:
                if alphanumeric_pattern.fullmatch(line) is not None:
                    valid_lines_temp.append(line)
            valid_lines = []
            for line in valid_lines_temp:
                if "government" in line.lower() or 'india' in line.lower():
                    continue 
                else:
                    valid_lines.append(line)

            if len(valid_lines) >= 2:
                data['name'] = valid_lines[0]
                data['aadhar_no'] = valid_lines[1]

            form = AadharUploadForm(initial={'name' : data['name'], 'dob' : datetime_str, 'aadhar_no' : data['aadhar_no'], 'gender' : data['gender']})
            response = render(request, 'aadhar_details.html', {'form' : form})
            response.set_cookie('name', data['name'])
            response.set_cookie('dob', datetime_str)
            response.set_cookie('aadhar_no', data['aadhar_no'])
            response.set_cookie('gender', data['gender'])
            return response
        elif "details" in request.POST:
            stored_name = request.COOKIES.get("name")
            stored_dob = request.COOKIES.get("dob")
            stored_aadhar_no = request.COOKIES.get("aadhar_no")
            stored_gender = request.COOKIES.get("gender")
            name = request.POST["name"]
            dob = request.POST["dob"]
            aadhar_no = request.POST["aadhar_no"]
            gender = request.POST["gender"]

            aadhar_model = AadharCandidate(name=name, dob=dob, aadhar_no=aadhar_no, gender=gender)
            if name != stored_name or dob != stored_dob or aadhar_no != stored_aadhar_no or gender != stored_gender:
                print(dob, stored_dob)
                aadhar_model.validationRequired = True
            aadhar_model.save()
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