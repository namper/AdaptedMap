from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from map.models import Marker
from map.serializers import MarkerSerializer, LongLatSerializer


class MarkerListView(ModelViewSet):
    queryset = Marker.objects.prefetch_related('images', )
    serializer_class = MarkerSerializer
    authentication_classes = []
    permission_classes = []

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
