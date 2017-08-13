from rest_framework import routers
from django.conf.urls import include, url
from cardtel.api.v1 import api

# router = routers.DefaultRouter()
# router.register(r'games', api.GameListView.as_view({'get': 'list'}), base_name='get')

# urlpatterns = [
#     url(r'^games/$', include(router.urls)),
# ]

urlpatterns = [
    url(r'^games/$', api.GameListView.as_view()),
]