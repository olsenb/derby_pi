from django.conf.urls import url, patterns

from views import RaceList, RaceDetail, CarList, CarDetail, AddCar, ScoreForm
urlpatterns = patterns(
    "",
    url(r'^$', RaceList.as_view(), name="races"),
    url(r'^race/(?P<pk>\d+)/$', RaceDetail.as_view(), name="race"),
    url(r'^race/(?P<race>\d+)/(?P<round>\d+)/(?P<heat>\d+)/$', ScoreForm.as_view(), name="race-score"),
    url(r'^race/(?P<pk>\d+)/(?P<round>\d+)/$', RaceDetail.as_view(), name="race-round"),
    url(r'^join/$', AddCar.as_view(), name="car-create"),
    url(r'^cars/$', CarList.as_view(), name="cars"),
    url(r'^cars/(?P<pk>\d+)/$', CarDetail.as_view(), name="car"),
)