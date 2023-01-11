from rest_framework import serializers
from ..models import FishPond, Device, Record
# from account.serializers import


class FishPondRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishPond
        fields = ['owner', 'location']


class ListDeviceOfFishPondSerializer(serializers.Serializer):
    fishPond = serializers.CharField(required=True)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['fishPond', 'createdAt']


class createRecordSerializer(serializers.ModelSerializer):
    # device = serializers.CharField(max_length=10)
    dissolved_oxygen = serializers.CharField(max_length=10, required=False)
    humidity = serializers.CharField(max_length=10, required=False)
    temperature = serializers.CharField(max_length=10, required=False)
    ph = serializers.CharField(max_length=10, required=False)
    evaluation = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = Record
        fields = ['device', 'dissolved_oxygen',
                  'humidity', 'temperature', 'ph', 'evaluation']

    def create(self, aquaticInformation):
        return Record.objects.create(**aquaticInformation)


# class GetRecordSerializer:
class FishPondSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(max_length=10)
    fishPondId = serializers.CharField(max_length=10)
    # errors = {}

    class Meta:
        model = FishPond
        fields = ['owner', 'fishPondId']

    def is_valid(self, raise_exception=False):
        if super(FishPondSerializer, self).is_valid():
            fishPond = FishPond.objects.get(id=self.data['fishPondId'])
            if fishPond:
                print(fishPond.owner.id, fishPond.owner.id == int(
                    self.data['owner']), self.data['owner'], type(fishPond.owner.id), type(self.data['owner']))
                if fishPond.owner.id == int(self.data['owner']):
                    return True
                else:
                    # self.data.errors['fishPond'] = 'you are not owner of this fishPond'
                    return False
            else:
                # self.data.errors.fishPond = 'this fishpond is not exist'
                return False


class RecordSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(max_length=10)
    deviceId = serializers.CharField(max_length=10)
    # errors = {}

    class Meta:
        model = Device
        fields = ['owner', 'deviceId']

    def is_valid(self, raise_exception=False):
        if super(RecordSerializer, self).is_valid(raise_exception):
            device = Device.objects.get(id=self.data['deviceId'])
            if device:
                fishPond = FishPondSerializer(data={
                    'owner': self.data['owner'], 'fishPondId': device.fishPond_id
                })
                if fishPond.is_valid():
                    return True
                else:
                    # self.data.errors = fishPond.data.errors
                    return False

            else:
                # self.data.errors['device'] = "this device is not exist"
                return False
        else:
            # self.data.errors = super(RecordSerializer, self).errors
            return False


class MakingResponseRecordSerializer(serializers.Serializer):
    device = serializers.CharField(max_length=10)
    create_date = serializers.DateField()
    dissolved_oxygen = serializers.CharField(max_length=10)
    humidity = serializers.CharField(max_length=10)
    temperature = serializers.CharField(max_length=10)
    ph = serializers.CharField(max_length=10)
    evaluation = serializers.CharField(max_length=30)


class MakingResponseFishPondSerializer(serializers.Serializer):
    owner = serializers.CharField(max_length=20)
    location = serializers.CharField(max_length=20)
