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
from Client.models import Profile,Ticket,Payment
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
        token_dict={"token":token.key}
        print("token is ",token)
        return Response({"token":token_dict},status=201)
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
        return Response({"token":token_dict})
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_detail(request):
    user_data={}
    obj=User.objects.get(pk=request.user.id)
    serializer=RegisterSerializer(obj)
    data=serializer.data
    print("here data is ",data)
    user_data['email']=data['email']
    user_data['usernmae']=data['username']
    user_data['phone']=data['phone']
    user_data['address']=data['address']
    user_data['date_of_birth']=data['date_of_birth']
    return Response({'User':user_data},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ticket_detail(request):
    user_obj=User.objects.get(id=request.user.id)
    if user_obj is not None:
        tick_detail=[]
        ticket_obj=Ticket.objects.filter(user=user_obj)
        for val in ticket_obj:
            temp={}
            ticket_serializer=TicketSerializer(val)
            pay_obj=Payment.objects.get(ticket=val)
            pay_serializer=PaymentSerializer(pay_obj)
            temp['source']=ticket_serializer.data['source']
            temp['destination']=ticket_serializer.data['destination']
            temp['bus_no']=ticket_serializer.data['bus_no']
            temp['price']=pay_serializer.data['price']
            temp['mode']=pay_serializer.data['mode']
            temp['date']=ticket_serializer.data['date']
            print("temp dict is ",temp)
            tick_detail.append(temp)
            # tick_detail={**tick_detail,**temp}
        print("Ticket detail is ",*tick_detail)
        return Response({"ticket_detail":tick_detail},status=200)
    return Response({"error":"User is not logged in!"})