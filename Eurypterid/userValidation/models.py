from django.db import models

from django.core.validators import MinLengthValidator

# Create your modelss here.

class AadharCandidate(models.Model):

    file = models.FileField()
    name = models.CharField(max_length=50)
    dob = models.DateField()
    aadhar_no = models.CharField(max_length=14)

class GateCandidate(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=13)
    dob = models.DateField()
    paper = models.TextField()
    gate_score = models.IntegerField()
    air = models.IntegerField()
    marks = models.DecimalField(max_digits=5, decimal_places=2)