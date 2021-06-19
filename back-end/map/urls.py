from django.urls import include, path
from rest_framework.routers import SimpleRouter

from map.views import MarkerListView

router = SimpleRouter()
router.register('markers', MarkerListView)

urlpatterns = [
    path('', include(router.urls)),
]
