from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins

from map.models import Marker, MarkerImage
from map.serializers import MarkerSerializer, LongLatSerializer, MarkerImageSerializer, CreateMarkerSerializer


class MarkerListView(ModelViewSet):
    queryset = Marker.objects.prefetch_related('images', )
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        serializer_class = MarkerSerializer
        if getattr(self, 'action', None) == 'create':
            serializer_class = CreateMarkerSerializer

        return serializer_class

    @action(detail=False, methods=('post',), url_path='getClosestMarkers', serializer_class=LongLatSerializer)
    def get_closest_markers(self, request):
        context = self.get_serializer_context()
        serializer = LongLatSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        queryset = Marker.objects.closest(
            data['lat'], data['lng']
        )

        serializer = MarkerSerializer(queryset, many=True)
        return Response(serializer.data)


class MarkerImageView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = MarkerImageSerializer
    queryset = MarkerImage.objects.all()
