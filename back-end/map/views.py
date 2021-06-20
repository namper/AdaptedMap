from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins

from map.models import Marker, MarkerImage
from map.serializers import MarkerSerializer, LongLatSerializer, CreateMarkerSerializer, \
    CreateMarkerImageSerializer


class MarkerListView(ModelViewSet):
    queryset = Marker.objects.prefetch_related('images', )
    authentication_classes = []
    permission_classes = []
    serializer_class = MarkerSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateMarkerSerializer(data=request.data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    serializer_class = CreateMarkerImageSerializer
    queryset = MarkerImage.objects.all()
    authentication_classes = []
    permission_classes = []
