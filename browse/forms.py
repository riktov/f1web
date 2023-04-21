"""Forms for the browse app"""
from django import forms
from f1web.models import Season, DrivingContract

class AddDriverDriveForm(forms.ModelForm):
    """Form form for adding a new Drive (year and team) to a driver detail"""
    class Meta:
        model = DrivingContract
        fields = [ "season", "team", "driver" ]

    # https://yu-nix.com/archives/django-form-get-val/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].widget = forms.HiddenInput()

class AddSeasonDriveForm(forms.ModelForm):
    """Form form for adding a new Drive (year and team) to a driver detail"""
    class Meta:
        model = DrivingContract
        fields = [ "season", "team", "driver" ]

    # https://yu-nix.com/archives/django-form-get-val/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['season'].widget = forms.HiddenInput()

class AddCarSeasonForm(forms.ModelForm):
    """Form for adding a new Season to a Car detail"""
    class Meta:
        model = Season
        fields = [ "year", "cars" ]

