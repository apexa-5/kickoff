from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('email','password')

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)
    


class CostumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costume
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'costume', 'start_date', 'end_date']  

