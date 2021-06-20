from django.urls import include, path
from rest_framework.routers import SimpleRouter

from map.views import MarkerListView, MarkerImageView

router = SimpleRouter()
router.register('markers', MarkerListView)
router.register('markerImages', MarkerImageView)

urlpatterns = [
    path('', include(router.urls)),
]
