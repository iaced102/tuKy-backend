from .. serializers.fishPond import FishPondRegisterSerializer, createRecordSerializer, RecordSerializer, MakingResponseRecordSerializer, MakingResponseFishPondSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from device.models import Record, FishPond, Device
from rest_framework.response import Response
import json


class FishPondRegisterView(APIView):
    def post(self, request):
        serializer = FishPondRegisterSerializer(
            data={'owner': request.user.id, 'location': request.data['location']})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Register successful!'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FishPondRecordValue(APIView):
    def post(self, request):

        # gửi dữ liệu từ thiết bị
        serializer = createRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Report successful!'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # lấy dữ liệu theo id thiết bị
        serializer = RecordSerializer(data={
            'owner': request.user.id, 'deviceId': request.data['deviceId']
        })
        if serializer.is_valid():
            indexFrom = 0
            indexTo = 5
            if hasattr(request.data, 'from'):
                indexFrom = request.data['from']
            if hasattr(request.data, 'to'):
                indexTo = request.data['to']
            queries = Record.objects.filter(id=request.data['deviceId'])[
                indexFrom:indexTo]
            device = Device.objects.get(id=request.data['deviceId'])
            print(device.fishPond_id)
            value = MakingResponseRecordSerializer(queries, many=True).data
            fishPond = MakingResponseFishPondSerializer(
                FishPond.objects.get(id=device.id)).data
            print(value, fishPond)
            # print(type(fishPond))
            data = {
                'value': value,
                'fishPond': json.dumps(fishPond),
                'deviceId': request.data['deviceId']
            }
            return Response(data, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'this device is not exist or you are not owner of this fishpond'}, status=status.HTTP_400_BAD_REQUEST)


class GetFishPondByUser(APIView):
    def get(self, request):
        if request.user:
            print(FishPond.objects.filter(owner_id=request.user.id))
            fishPond = MakingResponseFishPondSerializer(
                FishPond.objects.filter(owner_id=request.user.id), many=True).data
            return Response(fishPond, status=status.HTTP_200_OK)
