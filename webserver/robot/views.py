from robot.serializers import MoveCommandSerializer, MoveArmCommandSerializer, CameraPositionSerializer, LedStateSerializer, TextToSpeachSerializer
from robot.controller import Controller
from robot.camera import Camera

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import StreamingHttpResponse


class RobotViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def status(self, request):
        return Response({
            'status': 'OK',
            'robot': Controller.serialize()
        })

    @action(detail=False, methods=['post'])
    def move(self, request):
        serializer = MoveCommandSerializer(data=request.data)
        if serializer.is_valid():
            Controller.move(serializer.data['direction'],
                            serializer.data['speed'],
                            serializer.data['heading'],
                            serializer.data['duration'],
                            serializer.data['reset_camera'])
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def moves(self, request):
        serializer = MoveCommandSerializer(data=request.data, many=True)
        if serializer.is_valid():
            Controller.moves(serializer.data)
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def move_arm(self, request):
        serializer = MoveArmCommandSerializer(data=request.data)
        if serializer.is_valid():
            Controller.move_arm(elbow_angle=serializer.data['elbow_angle'], claw_angle=serializer.data['claw_angle'])
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_camera_position(self, request):
        serializer = CameraPositionSerializer(data=request.data)
        if serializer.is_valid():
            Controller.set_camera_position(serializer.data['x'],
                                           serializer.data['y'])
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_led_state(self, request):
        serializer = LedStateSerializer(data=request.data)
        if serializer.is_valid():
            Controller.set_led_state(serializer.data['left_on'],
                                     serializer.data['left_color'],
                                     serializer.data['right_on'],
                                     serializer.data['right_color'])
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def say(self, request):
        serializer = TextToSpeachSerializer(data=request.data)
        if serializer.is_valid():
            Controller.say(serializer.data['text'])
            return Response({
                'status': 'OK',
                'robot': Controller.serialize()
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def voices(self, request):
        return Response({
            'status': 'OK',
            'voices': Controller.get_voices()
        })

    @action(detail=False, methods=['get'])
    def get_distance_map(self, request):
        return Response({
            'status': 'OK',
            'map': Controller.get_distance_map()
        })

    @action(detail=False, methods=['get'])
    def stream(self, request):
        return StreamingHttpResponse(Camera.stream(),
                                     content_type="multipart/x-mixed-replace;boundary=FRAME")
