from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from .forms import AadharUploadForm
from .forms import GateUploadForm

from .models import GateCandidate

def aadhar_upload(request):
    if request.method == 'POST':
        form = AadharUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data['file'])
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