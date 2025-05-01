from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,generics, permissions
from .tasks import test_func
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Category,Costume,Image
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsCustomerUser,IsAdminUserStaff,IsBookingOwner


import sys
print("Python executable:", sys.executable)


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'})
        return Response(serializer.errors)

class Login(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

def image_view(request):
    costumes = Category.objects.prefetch_related('costume_set').all()
    return render(request, 'users/image_upload.html', {'costumes': costumes})

def image_upload(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        category_id = request.POST['costume']
        print(category_id,"category_id")
        costume = Costume.objects.get(id=category_id)
        print(costume,"9880980980898098989")

        for image in images:
            Image.objects.create(costume=costume, image=image)

        return HttpResponse('Images uploaded successfully')
    costumes = Category.objects.all()
    return render(request, 'users/image_upload.html',{'costumes': costumes})


@permission_classes([IsAdminUser])
class CostumeCRUD(viewsets.ModelViewSet):
    queryset = Costume.objects.all()
    serializer_class = CostumeSerializer
    filterset_fields = ['category']  
    ordering_fields = ['price']      
    # permission_classes = [IsAdminUser]




    def get_permissions(self):
            if self.action in ['list', 'retrieve']:
                return [AllowAny()]
            return [IsAdminUser()]


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
 
        # test_user = UserProfile.objects.first()
        serializer.save(user=request.user)
        return Response({'message': 'Costume booked succesfully '})
    return Response(serializer.errors, status=400)


from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAdminUserStaff])
def bookings_by_date(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    bookings = Booking.objects.all()
    if start_date:
        bookings = bookings.filter(start_date__gte=start_date)
    if end_date:
        bookings = bookings.filter(end_date__lte=end_date)

    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


def test(request):
    test_func.delay()

from rest_framework.generics import RetrieveUpdateDestroyAPIView

class BookingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwner]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .paypal_utils import get_paypal_access_token
from django.conf import settings
import requests

@api_view(['POST'])
def create_paypal_order(request):
    access_token = get_paypal_access_token()
    url = f'{settings.PAYPAL_BASE_URL}/v2/checkout/orders'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "10.00"  # dynamic value if needed
            }
        }],
        "application_context": {
           "return_url": "http://localhost:8000/paypal-success/",
            "cancel_url": "http://localhost:8000/paypal-cancel/"

        }
    }

    response = requests.post(url, headers=headers, json=data)
    return Response(response.json())



@api_view(['POST'])
def capture_paypal_order(request):
    order_id = request.data.get('order_id')  # Get order_id from frontend/mobile
    access_token = get_paypal_access_token()

    url = f'{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers)
    return Response(response.json())


def paypal_success(request):
    token = request.GET.get("token")
    payer_id = request.GET.get("PayerID")
    
    # Use the token to capture the payment via PayPal API here
    return HttpResponse("Payment successful!")

def paypal_cancel(request):
    return HttpResponse("Payment canceled.")


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)