from .. serializers.fishPond import DeviceSerializer, ListDeviceOfFishPondSerializer,ReportSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from ..models import FishPond, Device, Record
from django.db.models import Max, Q, Min, Sum, Avg
from datetime import date, timedelta


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


class GetDataForReport(APIView):
    def get(self, request):
        print(request.data)
        #groupBy chấp nhận 3 giá trị month, week, year
        groupBy = request.data['groupBy']
        # agg chấp nhận các giá trị gồm min, max, average,sum, nếu là min và max thì phải truyền thêm 1 trường nữa để xác định là cái gì min, max
        field = request.data['field']
        agg = request.data['agg']
        device = request.data['device']
        # số chu kì lấy ra
        cycle = request.data['cycle']
        today = date.today()
        records = []
        cycleValue =-1
        if groupBy=='week':
            cycleValue=7
        elif groupBy=='month':
            cycleValue=30
        elif groupBy=='year':
            cycleValue=365

        for i in range(cycle):
            # print(cycleValue)
            start_date = today - timedelta(days=cycleValue * i)
            end_date = start_date + timedelta(days=cycleValue)
            record_filter = Record.objects.filter(Q(create_date__gte=start_date) & Q(create_date__lt=end_date))
            record_chunk=[]
            if agg == 'max':
                value = record_filter.aggregate(Max(field))[field+'__'+agg]
                record_chunk = Record.objects.filter(Q(create_date__gte=start_date) & Q(create_date__lt=end_date) & Q(**{field: value}))
                for re in list(record_chunk.values()):
                    records.append(re)
                    break
            if agg =='min':
                value = record_filter.aggregate(Min(field))[field+'__'+agg]
                record_chunk = Record.objects.filter(Q(create_date__gte=start_date) & Q(create_date__lt=end_date) & Q(**{field: value}))
                for re in list(record_chunk.values()):
                    records.append(re)
                    break
            if agg =='sum':
                record_chunk = Record.objects.filter(Q(create_date__gte=start_date) & Q(create_date__lt=end_date)).aggregate(Sum('ph'),Sum('humidity'),Sum('evaluation'),Sum('temperature'), Sum('dissolved_oxygen'))
                # print(min_value)
                records += record_chunk
                records.append(record_chunk)
            if agg =='average':
                record_chunk = Record.objects.filter(Q(create_date__gte=start_date) & Q(create_date__lt=end_date)).aggregate(Avg('ph'),Avg('humidity'),Avg('evaluation'),Avg('temperature'), Avg('dissolved_oxygen'))
                print(record_chunk)
                # records += record_chunk
                records.append(record_chunk)
        return JsonResponse({
            'message':'oke',
            'data': list(records)
        }, status = status.HTTP_200_OK)