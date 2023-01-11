from .. serializers.fishPond import DeviceSerializer, ListDeviceOfFishPondSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from ..models import FishPond, Device
from datetime import date


class DeviceRegisterView(APIView):
    def post(self, request):
        if(request.user.is_superuser):
            # chỉ có superuser mới được quyền thêm một thiết bị
            print(request.data)
            serializer = DeviceSerializer(
                data={'fishPond': request.data["fishPond"], 'createdAt': date.today()})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Register successful!'}, status=status.HTTP_201_CREATED)
            return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': "you are not superUser, don't have permission"}, status=status.HTTP_401_UNAUTHORIZED)


class AllDeviceOfFishPond(APIView):
    def get(self, request):
        print(request.data)
        serializer = ListDeviceOfFishPondSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        fishpond = FishPond.objects.get(pk=request.data["fishPond"])
        devices = Device.objects.filter(
            fishPond=request.data['fishPond']).values()
        return JsonResponse({'message': 'oke', 'data': list(devices), }, status=status.HTTP_200_OK)
        # user =
