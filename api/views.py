from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from editor.models import Path, Point
from .serializers import PathSerializer, PointSerializer
from functools import wraps
from django.db import IntegrityError
from rest_framework import serializers


def swagger_safe_queryset(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        return func(self, *args, **kwargs)

    return wrapper


class PathViewSet(viewsets.ModelViewSet):
    serializer_class = PathSerializer
    queryset = Path.objects.all()

    @swagger_safe_queryset
    def get_queryset(self):
        return Path.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    queryset = Point.objects.all()

    @swagger_safe_queryset
    def get_queryset(self):
        return Point.objects.filter(
            path__user=self.request.user, path=self.kwargs["path_pk"]
        )

    def perform_create(self, serializer):
        path = get_object_or_404(
            Path, id=self.kwargs["path_pk"], user=self.request.user
        )
        try:
            serializer.save(path=path)
        except IntegrityError:
            raise serializers.ValidationError(
                "A point with this order already exists for this path."
            )
