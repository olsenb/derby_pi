from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django import forms
from models import Car, Race, CarTime


class RaceList(ListView):
    model = Race
    context_object_name = "races"


CarTimeFormset = forms.models.modelformset_factory(CarTime, fields=('finish_position', 'time'), extra=0)


class ScoreForm(FormView):
    form_class = CarTimeFormset
    template_name = "derby/score.html"

    def get_form_kwargs(self):
        self.race = Race.objects.get(pk=self.kwargs.get('race'))

        kwargs = super(ScoreForm, self).get_form_kwargs()
        kwargs['queryset'] = CarTime.objects.filter(
            race=self.race,
            round=self.kwargs.get('round'),
            heat=self.kwargs.get('heat'))
        return kwargs

    def form_valid(self, form):
        form.save()
        if self.race.current_round == int(self.kwargs.get('round')) and self.race.current_heat == int(self.kwargs.get('heat')):
            self.race.set_next_heat()
        return HttpResponseRedirect(self.race.get_absolute_url())


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


