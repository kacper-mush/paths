from editor.models import Path, Point
from rest_framework import serializers


class PathSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Path
        fields = ['id', 'user', 'name', 'background']


class PointSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='path.user.username')

    class Meta:
        model = Point
        fields = ['id', 'user', 'x', 'y', 'order']
