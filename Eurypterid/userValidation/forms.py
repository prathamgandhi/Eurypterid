from django import forms

class AadharUploadForm(forms.Form):
    file = forms.FileField()
    name = forms.CharField(max_length=50)
    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    aadhar_no = forms.CharField(max_length=14)
    gender = forms.CharField(max_length=10)
class GateUploadForm(forms.Form):
    file = forms.FileField()
    name = forms.CharField(max_length=50)
    parent_name = forms.CharField(max_length=50)
    reg_no = forms.CharField(max_length=13)
    paper = forms.CharField(widget=forms.Textarea)
    gate_score = forms.IntegerField()
    air = forms.IntegerField()
    marks = forms.DecimalField(max_digits=5, decimal_places=2)