from django.contrib import admin, messages

from models import *


class CarAdmin(admin.ModelAdmin):
    list_display = ['racer', 'number','name', 'division', 'weight']
    search_fields = ['racer', 'number']
    list_filter = ['division']


class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'lanes', 'current_heat']
    actions = ['start_race']

    def start_race(self, request, queryset):
        for race in queryset.filter(current_heat=0):
            race.generate_race()
            race.current_heat = 1
            race.current_round = 1
            race.save()
            messages.success(request, "Started Race %s" % race)


class CarTimeAdmin(admin.ModelAdmin):
    list_display = ['round', 'heat', 'lane', 'car', 'finish_position', 'time', 'race']
    list_filter = ['race', 'round', 'heat', 'lane']


admin.site.register(Race, RaceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Division)
admin.site.register(Awards)
admin.site.register(CarAwards)
admin.site.register(CarTime, CarTimeAdmin)
