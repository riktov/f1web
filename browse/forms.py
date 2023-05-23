"""Forms for the browse app"""
from django import forms
from f1web.models import Car, Season, DrivingContract

class CreateDriveForm(forms.ModelForm):
    """Form form for creating a new Drive (driver, team, season)"""
    class Meta:
        model = DrivingContract
        fields = [ "season", "team", "driver", "is_lead" ]

class CreateDriveForThisDriverForm(CreateDriveForm):
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

class AddThisCarToSeasonForm(forms.ModelForm):
    """Form for adding a Car in a detail view to a Season"""
    #We base it on the Season model only to conveniently get a list of years 
    # We do not create a Season object
    class Meta:
        model = Season
        fields = [ "year"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.fields['cars'].widget = forms.HiddenInput()

class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['constructor', 'slug']
