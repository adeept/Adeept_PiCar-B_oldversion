from rest_framework import serializers


class MoveCommandSerializer(serializers.Serializer):
    direction = serializers.CharField(max_length=1, choices=['F', 'B', 'S'])
    float = serializers.FloatField(max_value=0.0, min_value=0.0)
