from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from AdaptedMap.utils import CustomVersatileImageFieldSerializer
from map.models import Marker, MarkerImage


class MarkerImageSerializer(ModelSerializer):
    image = CustomVersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('slider', 'crop__431x431'),
        ]
    )

    class Meta:
        model = MarkerImage
        fields = ('id', 'image')


class CreateMarkerImageSerializer(ModelSerializer):
    class Meta:
        model = MarkerImage
        fields = ('id', 'image', 'marker')


class MutateMarkerImageSerializer(ModelSerializer):
    class Meta:
        model = MarkerImage
        fields = ('id', 'image')
        extra_kwargs = {
            'image': {'required': True}
        }


class MarkerSerializer(ModelSerializer):
    images = MarkerImageSerializer(many=True)
    distance = SerializerMethodField()

    def get_distance(self, obj):
        return getattr(obj, 'distance', None)

    class Meta:
        model = Marker
        fields = ('id', 'lat', 'lng', 'images', 'name', 'distance')


class CreateMarkerSerializer(ModelSerializer):
    image = MutateMarkerImageSerializer(source='images', many=True)

    def create(self, validated_data):
        images = validated_data.pop('images', None)
        marker = super().create(validated_data)
        if images:
            MarkerImage.objects.create(**images[0], marker=marker)
        return marker

    class Meta:
        model = Marker
        fields = ('id', 'name', 'lat', 'lng', 'image')


class LongLatSerializer(ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'lat', 'lng',)
