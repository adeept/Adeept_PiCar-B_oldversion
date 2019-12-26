from rest_framework import serializers


class MoveCommandSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=['F', 'B', 'S'])
    speed = serializers.FloatField(min_value=0.0, max_value=100.0)
