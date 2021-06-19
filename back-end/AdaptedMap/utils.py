from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.utils import build_versatileimagefield_url_set


class CustomVersatileImageFieldSerializer(VersatileImageFieldSerializer):
    def to_native(self, value):
        """For djangorestframework <=2.3.14"""
        context_request = None
        if self.context:
            context_request = self.context.get('request', None)
            if context_request.get_host() == "back":
                context_request = None
        return build_versatileimagefield_url_set(
            value,
            self.sizes,
            request=context_request
        )
