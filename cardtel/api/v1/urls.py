from django.conf.urls import include, url
from cardtel.api.v1 import api


urlpatterns = [
    url(r'^games/$', api.GameListView.as_view()),
]s