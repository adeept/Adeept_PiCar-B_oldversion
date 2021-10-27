from rest_framework import serializers


class MoveCommandSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=['F', 'B', 'S'], default='S')
    speed = serializers.FloatField(min_value=0.0, max_value=100.0, default=0.0)
    duration = serializers.FloatField(min_value=0.0, default=1.0)
    heading = serializers.FloatField(min_value=-90.0, max_value=90.0, default=0.0)


class CameraPositionSerializer(serializers.Serializer):
    x = serializers.FloatField(min_value=-90.0, max_value=90.0, default=0.0)
    y = serializers.FloatField(min_value=-90.0, max_value=90.0, default=0.0)


class LedStateSerializer(serializers.Serializer):
    COLORS = [
        'white',
        'red',
        'green',
        'blue',
        'cyan',
        'pink',
        'yellow'
    ]
    left_on = serializers.BooleanField(default=False)
    left_color = serializers.ChoiceField(choices=COLORS, default='white')

    right_on = serializers.BooleanField(default=False)
    right_color = serializers.ChoiceField(choices=COLORS, default='white')
