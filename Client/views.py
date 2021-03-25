from django.shortcuts import render,redirect
from django.conf import settings
from rest_framework.response import Response 
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,UserDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from Client.serializers import TicketSerializer,PaymentSerializer
User = get_user_model()

@api_view(['POST'])
def create_profile(request):
    data=request.data or None
    print("serialized data is ",data)
    serializer=RegisterSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user_obj=User.objects.get(email=data['email'])
        token=Token.objects.get(user=user_obj)
        print("token is ",token)
        return Response(serializer.data,status=201)
    return Response({},status=400) 

@api_view(['POST'])
def login(request):
    data=request.data or None
    user = authenticate(email=data['email'], password=data['password'])
    print("user is ",user)
    if user is not None:
        serializer=UserDetailSerializer(user)
        print(serializer.data)
        token=Token.objects.get(user=user)
        token_dict={"token":token.key}
        data={**serializer.data,**token_dict}
        return Response({"data":data})
    return Response({'error':"Invalid username or password"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def access_data(request):
    return Response("Yes you are authenticated")

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ticket_booking(requests):
    data=requests.data or None
    print("before data is ",data)
    data['user']=requests.user.id
    tick_seri=TicketSerializer(data=data)
    if tick_seri.is_valid():
        tick_data=tick_seri.save()
        print("pay_data is ",tick_data.id)
        data['ticket']=tick_data.id
        pay_seri=PaymentSerializer(data=data)
        if pay_seri.is_valid():
            print("idhr aa rha hai kya")
            pay_seri.save()
            return Response({"ticket":"Booked Successfully"},status=201)
        print("ticket mei kya error hai ",tick_seri.errors)
    return Response({'Error':"Please send data in right format"},status=401)
