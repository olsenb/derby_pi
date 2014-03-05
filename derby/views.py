from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django import forms
from models import Car, Race


class RaceList(ListView):
    model = Race
    context_object_name = "races"


class RaceManager(forms.Form):
    pass


class RaceDetail(DetailView):
    model = Race
    context_object_name = "race"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "start" in self.request.POST:
            self.object.generate_race()
        return self.render_to_response(self.get_context_data())

class CarList(ListView):
    model = Car
    context_object_name = "cars"


class CarDetail(DetailView):
    model = Car
    context_object_name = "car"


class AddCar(CreateView):
    model = Car


