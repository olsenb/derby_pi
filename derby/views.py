from django.views.generic import ListView, DetailView, FormView, CreateView

from models import Car, Race


class RaceList(ListView):
    model = Race
    context_object_name = "races"


class RaceDetail(DetailView):
    model = Race
    context_object_name = "race"


class CarList(ListView):
    model = Car
    context_object_name = "cars"


class CarDetail(DetailView):
    model = Car
    context_object_name = "car"


class AddCar(CreateView):
    model = Car


