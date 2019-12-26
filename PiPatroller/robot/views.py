import robot.motor as motor
from robot.serializers import MoveCommandSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Initialization
motor.setup()


class RobotViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def move(self, request):
        serializer = MoveCommandSerializer(data=request.data)
        if serializer.is_valid():
            motor.move(serializer.data['direction'], serializer.data['speed'])
            return Response({'status': 'OK'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
