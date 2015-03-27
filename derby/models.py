import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.datastructures import SortedDict

from race import Ppn, RoundRobin


class Division(models.Model):
    name = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ('ordering',)

    def __unicode__(self):
        return self.name


class Car(models.Model):
    racer = models.CharField("Racer Name", max_length=100)
    number = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, help_text="Car Name")
    division = models.ForeignKey(Division)
    weight = models.FloatField(default="5.0", help_text="in Ounces")
    photo = models.ImageField(upload_to="car/", blank=True, null=True)

    class Meta:
        ordering = ('number', 'racer')

    def __unicode__(self):
        if self.name:
            return "#%d %s" % (self.number, self.name)
        return "#%d" % self.number

    @property
    def races(self):
        return Race.objects.filter(times__car=self).distinct()

    @property
    def best_time(self):
        try:
            return self.times.order_by('time')[0].time
        except IndexError:
            return None

    @property
    def avg_time(self):
        return self.times.aggregate(t=models.Avg('time'))['t']

    def get_absolute_url(self):
        return reverse('derby:car', kwargs={'pk': self.id})

RACE_CHOICES = (
    #('single', 'Single Elimination'),
    #('double', 'Double Elimination'),
    ('ppn', 'Practically Perfect N'),
    #('round', 'Round Robin'),
)


class Race(models.Model):
    name = models.CharField(max_length=100, help_text="ex. Pack 1234 2013")
    type = models.CharField(max_length=20, choices=RACE_CHOICES)
    lanes = models.IntegerField(default=3)
    rounds = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)
    current_heat = models.IntegerField(default=0)
    current_round = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("derby:race", kwargs={'pk': self.id})

    def get_score_url(self):
        return reverse("derby:race-score", kwargs={'race': self.id, 'round': self.current_round, 'heat': self.current_heat})

    def generate_race(self):
        if self.type == 'ppn':
            cls = Ppn
        elif self.type == 'round':
            cls = RoundRobin
        cars = list(Car.objects.all())
        race_type = cls(self.lanes, len(cars), self.rounds)
        rounds = race_type.generate_heats(self.rounds)

        self.rounds = len(rounds)
        self.save()

        for rnd, heats in enumerate(rounds, start=1):
            for heat, lanes in enumerate(heats, start=1):
                for lane, car in enumerate(lanes, start=1):
                    CarTime.objects.create(car=cars[car-1], lane=lane, race=self, round=rnd, heat=heat)
        return True

    def now_racing(self):
        return self.times.filter(heat=self.current_heat, round=self.current_round)

    def next_heat(self):
        if self.finished:
            return False
        heat = self.times.filter(heat=self.current_heat + 1, round=self.current_round)
        if not heat.count():
            heat = self.times.filter(heat=1, round=self.current_round + 1)
        return heat

    def set_next_heat(self):
        next_heat = self.next_heat()
        if next_heat.exists():
            car_time = next_heat[0]
            self.current_round = car_time.round
            self.current_heat = car_time.heat
            self.save()
            return True
        else:
            self.finished = datetime.datetime.now()
            self.current_heat = 0
            self.current_round = 0
            self.save()
            return False

    def results(self):
        totals = {}
        if self.finished:
            for cartime in self.times.filter(finish_position__gt=0):
                score = max(self.lanes+1 - cartime.finish_position, 0)
                if cartime.car not in totals:
                    totals[cartime.car] = 0
                totals[cartime.car] += score
            results = sorted(totals.items(), key=lambda x: x[1], reverse=True)
            divisions = SortedDict({'Overall': results})
            for d in Division.objects.all():
                divisions[d] = []
            for car, score in results:
                divisions[car.division].append((car, score))

            return divisions
        return False

    def __unicode__(self):
        return self.name


class CarTime(models.Model):
    """
    Track the car throughout the race
    A Race contains many Rounds
    A Round contains many Heats
    A Heat has up to as many racers as there are lanes
    """
    car = models.ForeignKey(Car, related_name="times")
    race = models.ForeignKey(Race, related_name="times")
    round = models.IntegerField(default=1)
    heat = models.IntegerField(default=1)
    lane = models.IntegerField(default=0)
    time = models.FloatField(blank=True, null=True)
    finish_position = models.IntegerField(null=True, blank=True)

    def get_score_url(self):
        return reverse("derby:race-score", kwargs={'race': self.race_id, 'round': self.round, 'heat': self.heat})

    class Meta:
        ordering = ('race', 'round', 'heat', 'lane')
    def __unicode__(self):
        return "%s %s" % (self.car, self.time)


class Awards(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Awards"

    def __unicode__(self):
        return self.name


class CarAwards(models.Model):
    car = models.ForeignKey(Car)
    award = models.ForeignKey(Awards)

    class Meta:
        verbose_name_plural = "Car Awards"
        ordering = ('car__number',)

    def __unicode__(self):
        return "%s %s" % (self.car, self.award)