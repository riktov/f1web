"""Views for the browse app"""
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView 
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
# from django.http import HttpResponse

from f1web.models import Car, Driver, Constructor, Season, Engine
from .forms import CreateDriveForThisDriverForm, AddThisCarToSeasonForm, CreateCarForm


# Create your views here.

def index(request):
    """View for top page in browse app"""
    return render(request, "browse/index.html", None)

class DriverDetailView(DetailView):
    """DetailView for Driver"""
    model = Driver

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateDriveForThisDriverForm(initial = {'driver': self.get_object() })
        return context
    
    def post(self, request, *args, **kwargs):
        """The form will never be initialized to an existing object"""
        incoming_form = CreateDriveForThisDriverForm(request.POST, request.FILES)

        if incoming_form.is_valid():
            # self.object = self.get_object()#this is the driver
            # context = super().get_context_data(**kwargs)
            # context['form'] = AddDriverDriveForm(initial = {'driver': self.get_object() })
        
            incoming_form.save()

            #for some reason we need to set this
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCarForm()
        context['seasons_table'] = self.get_object().seasons_and_cars_and_drivers()
        return context
    
class CarDetailView(DetailView):
    """DetailView for Car"""
    model = Car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddThisCarToSeasonForm()
        return context
    
    def post(self, request, *args, **kwargs):
        #Unlike CreateDriveForDriverForm, we are not creating a new model object 
        # (DrivingContract) which is then
        #hooked up to the existing objects (season, team, driver) with 
        # DB relational (ForeignKey) objects.
        #Here we are creating just a DB (ManyToMany) object which added.

        # Might be better to use UpdateView
        # https://stackoverflow.com/a/34460881/316698
        self.object = self.get_object()
        this_car = self.get_object()
        context = self.get_context_data(**kwargs)

        incoming_form = AddThisCarToSeasonForm(request.POST, request.FILES)

        year = request.POST['year']
        season = Season.objects.get(year = year)
        season.cars.add(this_car)
        season.save()

        
        #we need to get an "object" attribute on this view, the template looks for it    
        return self.render_to_response(context=context)

class CarUpdateView(UpdateView):
    model = Car
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddThisCarToSeasonForm()
        return context

    def post(self, request, *args, **kwargs):
        #Unlike CreateDriveForDriverForm, we are not creating a new model object 
        # (DrivingContract) which is then
        #hooked up to the existing objects (season, team, driver) with 
        # DB relational (ForeignKey) objects.
        #Here we are creating just a DB (ManyToMany) object which added.

        # Might be better to use UpdateView
        # https://stackoverflow.com/a/34460881/316698
        self.object = self.get_object()
        this_car = self.get_object()
        context = self.get_context_data(**kwargs)

        incoming_form = AddThisCarToSeasonForm(request.POST, request.FILES)

        year = request.POST['year']
        season = Season.objects.get(year = year)
        season.cars.add(this_car)
        season.save()

        
        #we need to get an "object" attribute on this view, the template looks for it    
        return self.render_to_response(context=context)

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
        context['seasons_list'] = Season.objects.all()
        return context



