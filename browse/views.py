"""Views for the browse app"""
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView 
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
# from django.http import HttpResponse

from browse.queries import single_driver_countries
from browse.scrape import scrape_season
from f1web.models import Car, ConstructorTransfer, Driver, Constructor, DrivingContract, EngineMaker, Season, Engine, CarNumber
from . forms import CreateDriveForThisDriverForm, AddThisCarToSeasonForm, CreateCarForm, CreateNumberForm
from . import tables

# Create your views here.

def index(request):
    """View for top page in browse app"""
    return render(request, "browse/index.html", None)

class DetailViewWithObjectList(DetailView):
    """An abstract view for a single object which always includes a list of other objects of the same class"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_object_list'] = self.model.objects.all()
        return context
    
class DriverDetailView(DetailView):
    """DetailView for Driver"""
    model = Driver

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateDriveForThisDriverForm(initial = {'driver': self.get_object() })
        context['drives_list'] = self.get_object().drives.all().order_by('season', 'starting_round')
        
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

class ConstructorDetailView(DetailViewWithObjectList):
    """DetailView for Constructor"""
    model = Constructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cons = self.get_object()  # Explicitly cast to Constructor

        context['form'] = CreateCarForm()
        context['cars_table'] = cons.cars_ordered_by_season()
        context['seasons_table'] = cons.seasons_and_cars_and_drivers()

        season_rows = []

        for season in Season.objects.filter(cars__constructor = cons).distinct():
            row = (season, 
                   season.cars.filter(constructor=cons), 
                   season.drives.filter(team=cons).order_by('starting_round', '-is_lead'), 
                   cons.car_numbers(season))
            season_rows.append(row)

        context['season_rows'] = season_rows
        
        context['previously'] = cons.previously.all()
        context['subsequently'] = cons.subsequently.all()
        # context['model_objects_list'] = self.model.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        # create a new Car by this Constructor
        self.object = self.get_object()
        name = request.POST['name']

        engine = None
        engine_id = request.POST['engine']
        if engine_id != '':
            engine = Engine.objects.get(pk = int(engine_id))

        constructor = self.get_object()
        car = Car(name = name, constructor = constructor, engine = engine)
        car.save()
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context=context)
    
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

class xxCarUpdateView(UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grouped_list'] = self.list_by_constructor()
        return context

    def list_by_constructor(self):
        """List of cars grouped by Constructor"""
        cons = {}
        #why does this return multiple instances of the same car if it appears in multiple_years?
        for car in Car.objects.all().order_by('season__year'):
            if car.constructor not in cons:
                cons[car.constructor] = []
            if car not in cons[car.constructor]:#cars appear only once, regardless of how many seasons
                cons[car.constructor].append(car)
        
        cons_keys = list(cons.keys())
        cons_keys.sort(key=lambda c: c.name)

        cars_grouped = [{'constructor':c, 'cars':cons[c]} for c in cons_keys]
        #now take the keys in cons, sort alphabetically, and create a list from the dictionary
        return cars_grouped

class EngineDetailView(DetailView):
    """DetailView for Engine"""
    model = Engine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars = self.get_object().car_set.all()

        #FIX Attribute error if none of the cars have seasons
        context['cars_grouped_by_season'] = tables.cars_grouped_by_season(cars)
        return context

class EngineListView(ListView):
    """ListView for Engine"""
    model = Engine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grouped_list'] = self.list_by_enginemaker()
        return context
    
    def list_by_enginemaker(self):
        engines_of = {}

        for em in EngineMaker.objects.all():
            engines = [e for e in em.engine_set.all()]  

            #This can be sorted by season with a template tag
            engines_of[em] = engines
        
        emakers_keys = list(engines_of.keys())
        emakers_keys.sort(key=lambda em: em.name)

        engines_grouped = [{'maker':em, 'engines':engines_of[em]} for em in emakers_keys]
        #now take the keys in cons, sort alphabetically, and create a list from the dictionary
        return engines_grouped


    
class EngineMakerDetailView(DetailViewWithObjectList):
    """Detail for for Engine Maker"""
    model = EngineMaker

class EngineMakerListView(ListView):
    model = EngineMaker
    #TODO The list of engines (object.engine_set) should be sorted by earliest season

class SeasonListView(ListView):
    """ListView for Season"""
    model = Season

class SeasonDetailView(DetailViewWithObjectList):
    """DetailView for Season"""
    model = Season
    def get_object(self) :
        if 'fetchwiki' in self.request.GET:
            constructor = self.request.GET['constructor']
            field = self.request.GET['field']

            cons = Constructor.objects.get(name = constructor)

            season = super().get_object()
            entrants = scrape_season(season.year)

            for entrant in entrants:
                if entrant['constructor']['name'] == constructor or entrant['entrant'] == constructor:
                    car_names = entrant['cars']
                    for car_name in car_names:
                        car = Car.objects.filter(name = car_name, constructor = cons)
                        if not car:
                            car = Car.objects.create(name = car_name, constructor = cons)
                            car.save()
                        else:
                            car = car.first()
                        season.cars.add(car)
                    season.save()

            
            #fetch data and write to database
        return super().get_object()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers_table'] = tables.team_car_drivers_for_season(self.get_object())
        context['rules'] = [ rule.description for rule in self.object.rule_set.all() ]


        transfers = ConstructorTransfer.objects.filter(season = self.get_object())
        context['transfers'] = transfers

        this_season_teams = [ car.constructor for car in self.object.cars.all() ]
        prev_season_teams = [ car.constructor for car in self.object.previous().cars.all() ]

        departing = [ cons for cons in prev_season_teams if cons not in this_season_teams]
        transferring_out = [ trans.previous for trans in transfers]
        departing = { cons for cons in departing if cons not in transferring_out }
        context['departing'] = departing 
        
        new_entrants = [ cons for cons in this_season_teams if cons not in prev_season_teams ]
        transferring_in = [ trans.new for trans in transfers]
        new_entrants = { cons for cons in new_entrants if cons not in transferring_in }
        
        context['new_entrants'] = new_entrants 

        # context['driver_histories'] = [ [dr] + dr.history(self.object) for dr in self.object.drivers()]
        return context

    def post(self, request, *args, **kwargs):
        #Unlike CreateDriveForDriverForm, we are not creating a new model object 
        # (DrivingContract) which is then
        #hooked up to the existing objects (season, team, driver) with 
        # DB relational (ForeignKey) objects.
        #Here we are creating just a DB (ManyToMany) object which added.

        self.object = self.get_object()
        this_year = self.get_object()
        context = self.get_context_data(**kwargs)

        team_id = request.POST['team']

        if 'number' in request.POST:
            incoming_form = CreateNumberForm(request.POST, request.FILES)

            number = request.POST['number']
            team = Constructor.objects.get(pk=team_id)

            number_obj = CarNumber(season = this_year, team=team, number=number)
            number_obj.save()

        if 'driver' in request.POST:
            # incoming_form = CreateNumberForm(request.POST, request.FILES)

            driver_id = request.POST['driver']
            team = Constructor.objects.get(pk=team_id)
            driver = Driver.objects.get(pk=driver_id)
            is_lead = 'is_lead' in request.POST and request.POST['is_lead'] == 'on'

            drive_obj = DrivingContract(season = this_year, team=team, driver=driver, is_lead=is_lead)
            drive_obj.save()

        # we need to get the context again before refreshing
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

class SeasonDriversDetailView(DetailViewWithObjectList):
    model = Season
    template_name = "f1web/season_drivers_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['driver_histories'] = [ [dr] + dr.history(self.get_object()) for dr in self.get_object().drivers()]
        return context
   

def countries_view(request):
    """A view of all countries with drivers and constructors"""
    countries_with_constructors = { c.country for c in Constructor.objects.all() }
    countries_with_drivers = { c.country for c in Driver.objects.all() }

    all_countries = countries_with_constructors.union(countries_with_drivers)

    all_countries = sorted(list(all_countries), key = lambda c: c.name)

    countries_grouped = [ (c, Constructor.objects.filter(country = c), Driver.objects.filter(country = c)) for c in all_countries ]
    return render(request, "browse/countries.html", {"country_list": countries_grouped})

def numbers_view(request):
    """A view of all the car numbers by season"""
    numbers = set([cn.number for cn in CarNumber.objects.filter(season__lt=1996)])

    seasons = Season.objects.filter(year__lt=1996)

    table = []

    for s in seasons:
        row = []

        carnums = {cn.number:cn for cn in CarNumber.objects.filter(season = s)}

        for num in numbers:
            row.append(carnums.get(num))
    
        table.append({"season":s, "numbers":row})
    return render(request, "browse/numbers.html", {"table": table, "numbers":numbers})

def season_driver_countries_view(request):
    all_countries = { dr.country for dr in Driver.objects.all() }

    singles = single_driver_countries()
    
    multiples = set()
    for c in all_countries:
        if c not in singles:
            multiples.add(c)

    context = {
        "multiples":multiples
    }
    return render(request, "browse/season_driver_countries.html", context)
