"""Views for the browse app"""
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django.http import HttpResponse
from django import forms

from f1web.models import Car, Driver, Constructor, Season, Engine, DrivingContract
from .forms import CreateDriveForDriverForm, CreateDriveForSeasonForm, AddSeasonToCarForm


# Create your views here.

def index(request):
    """View for top page in browse app"""
    return render(request, "browse/index.html", None)

class DriverDetailView(DetailView):
    """DetailView for Driver"""
    model = Driver

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateDriveForDriverForm(initial = {'driver': self.get_object() })
        return context
    
    def post(self, request, *args, **kwargs):
        """The form will never be initialized to an existing object"""
        incoming_form = CreateDriveForDriverForm(request.POST, request.FILES)

        if incoming_form.is_valid():
            # self.object = self.get_object()#this is the driver
            # context = super().get_context_data(**kwargs)
            # context['form'] = AddDriverDriveForm(initial = {'driver': self.get_object() })
        
            incoming_form.save()

            self.object = self.get_object()#this is the driver
            context = self.get_context_data(**kwargs)
        
            return self.render_to_response(context=context)
        else:
            return HttpResponse("Error")


class DriverListView(ListView):
    """ListView for Driver"""
    model = Driver

class ConstructorListView(ListView):
    """ListView for Constructor"""
    model = Constructor

class ConstructorDetailView(DetailView):
    """DetailView for Constructor"""
    model = Constructor

class CarDetailView(DetailView):
    """DetailView for Car"""
    model = Car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddSeasonToCarForm()
        return context
    
class CarListView(ListView):
    """ListView for Car"""
    model = Car

class EngineDetailView(DetailView):
    """DetailView for Engine"""
    model = Engine

class EngineListView(ListView):
    """ListView for Engine"""
    model = Engine

class SeasonListView(ListView):
    """ListView for Season"""
    model = Season

class SeasonDetailView(DetailView):
    """DetailView for Season"""
    model = Season

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['cars'] = self.object.cars.all()
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddSeasonToCarForm()
        return context