from django.contrib import admin

from .models import AadharCandidate, GateCandidate

admin.site.register(AadharCandidate)
admin.site.register(GateCandidate)