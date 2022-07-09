"""Custom mixins module for api app."""
from rest_framework import mixins, viewsets
from rest_framework.response import Response


class PatchModelMixin(object):
    """PATCH a model instance."""
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CustomListRetriveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Custom mixin for GET request only."""
    pass


class CustomCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Custom mixin for POST, DELETE request only."""
    pass


class RecipeMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    PatchModelMixin,
    viewsets.GenericViewSet
):
    """Custom mixin where PUT is not included."""
    pass
