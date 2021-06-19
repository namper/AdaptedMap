from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from AdaptedMap.utils import CustomVersatileImageFieldSerializer
from map.models import Marker


class MarkerImageSerializer(ModelSerializer):
    image = CustomVersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('slider', 'crop__431x431'),
            # ('slider_thumbnail', 'thumbnail__100x100'),
            # ('listing_thumbnail', 'crop__170x170')
        ]
    )

    class Meta:
        model = Marker
        fields = ('id', 'image')


class MarkerSerializer(ModelSerializer):
    images = MarkerImageSerializer(many=True)

    distance = SerializerMethodField()

    def get_distance(self, obj):
        return getattr(obj, 'distance', None)

    class Meta:
        model = Marker
        fields = ('id', 'lat', 'lng', 'images', 'name', 'distance')


class LongLatSerializer(ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'lat', 'lng',)
