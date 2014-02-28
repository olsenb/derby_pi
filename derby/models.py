from django.core.urlresolvers import reverse
from django.db import models


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
    front_photo = models.ImageField(upload_to="car/front/")
    side_photo = models.ImageField(upload_to="car/side/")

    def __unicode__(self):
        if self.name:
            return self.name
        return "%s" % self.number

    def get_absolute_url(self):
        return reverse('derby:car', kwargs={'pk': self.id})

RACE_CHOICES = (
    ('single', 'Single Elimination'),
    ('double', 'Double Elimination'),
    ('triple', 'Triple Elimination'),
    ('round', 'Round Robin'),
)


class Race(models.Model):
    name = models.CharField(max_length=100, help_text="ex. Pack 1234 2013")
    type = models.CharField(max_length=20, choices=RACE_CHOICES)
    lanes = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)

    def generate_heats(self):
        """
        Called after each heat if returns False then complete the race.
        """
        #TODO: create CarTime objects based on the race Choice and # of lanes

        return True

    def next_heat(self):
        self.times.filter(time__isnull=True)

    def __unicode__(self):
        return self.name


class CarTime(models.Model):
    heat = models.IntegerField(default=1)
    race = models.ForeignKey(Race, related_name="times")
    car = models.ForeignKey(Car, related_name="times")
    lane = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.car, self.time)


class Awards(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class CarAwards(models.Model):
    car = models.ForeignKey(Car)
    award = models.ForeignKey(Awards)

    def __unicode__(self):
        return "%s %s" % (self.car, self.award)