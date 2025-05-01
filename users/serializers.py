from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('name','email','password')

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)
    


class CostumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costume
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    costumes = CostumeSerializer(many=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'description', 'original_price', 'offer_price', 'costumes']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'costume', 'start_date', 'end_date']  


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,    
            'name':self.user.name       
        }

        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'costume', 'user', 'rating', 'comment']