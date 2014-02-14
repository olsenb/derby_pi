from django.conf.urls import url, patterns

from views import RaceList
urlpatterns = patterns(
    "",
    url(r'^$', RaceList.as_view(), name="races"),
)