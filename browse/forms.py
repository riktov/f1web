"""Forms for the browse app"""
from django import forms
from f1web.models import Season, DrivingContract

class CreateDriveForm(forms.ModelForm):
    """Form form for creating a new Drive (driver, team, season)"""
    class Meta:
        model = DrivingContract
        fields = [ "season", "team", "driver" ]

class CreateDriveForDriverForm(CreateDriveForm):
    """Form form for creating a new Drive for an already specified driver"""
    # https://yu-nix.com/archives/django-form-get-val/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].widget = forms.HiddenInput()

class CreateDriveForSeasonForm(CreateDriveForm):
    """Form form for creating a new Drive for a specified season"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['season'].widget = forms.HiddenInput()

class AddSeasonToCarForm(forms.ModelForm):
    """Form for adding a new Season to a Car detail"""
    class Meta:
        model = Season
        fields = [ "year", "cars" ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget = forms.HiddenInput()
