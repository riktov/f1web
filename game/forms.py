from django import forms
from f1web.models import Driver


class DriverSelectionForm(forms.Form):
    driver_from = forms.ModelChoiceField(queryset=Driver.objects.all())
    driver_to = forms.ModelChoiceField(queryset=Driver.objects.all())
