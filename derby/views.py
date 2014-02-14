from django.views.generic import ListView, DetailView

from models import Car, Race


class RaceList(ListView):
    model = Race


class RaceDetails(DetailView):
    model = Race

class CarDetail(DetailView):
    model = Car