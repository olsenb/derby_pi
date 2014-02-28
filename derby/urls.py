from django.conf.urls import url, patterns

from views import RaceList, RaceDetail, CarList, CarDetail, AddCar
urlpatterns = patterns(
    "",
    url(r'^$', RaceList.as_view(), name="races"),
    url(r'^race/(?P<pk>\d+)/$', RaceDetail.as_view(), name="race"),
    url(r'^join/$', AddCar.as_view(), name="car-create"),
    url(r'^cars/$', CarList.as_view(), name="cars"),
    url(r'^cars/(?P<pk>\d)/$', CarDetail.as_view(), name="car"),
)