from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Category,Costume,Image
from rest_framework.decorators import api_view, permission_classes

class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'})
        return Response(serializer.errors)

class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


def image_view(request):
    costumes = Category.objects.all()
    return render(request,'users/image_upload.html',{'costumes': costumes})



def image_upload(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        print(images,"898989898989898989")
        costume_id = request.POST['costume']
        costume = Costume.objects.get(id=costume_id)

        for image in images:
            Image.objects.create(costume=costume, image=image)

        return HttpResponse('Images uploaded successfully')
    costumes = Costume.objects.all()
    return render(request, 'users/image_upload.html', {'costumes': costumes})


class CostumeCRUD(viewsets.ModelViewSet):
    queryset = Costume.objects.all()
    serializer_class = CostumeSerializer
    permission_classes = [IsAdminUser]



@api_view(['GET'])
def view_packages(request):
    packages = Package.objects.all()
    serializer = PackageSerializer(packages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def book_costume(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        start = serializer.validated_data['start_date']
        end = serializer.validated_data['end_date']
        costume = serializer.validated_data['costume']

        check_aval= Booking.objects.filter(costume=costume, start_date__lt=end, end_date__gt=start)
        if check_aval.exists():
            return Response({'error': 'Sorry costume not available for these dates'}, status=400)

        serializer.save(user=request.user)
        return Response({'message': 'Costume booked succesfully '})
    return Response(serializer.errors, status=400)

