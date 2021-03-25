
from rest_framework import serializers
from django.conf import settings
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Ticket,Payment
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','username','phone','password','address','date_of_birth']
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(RegisterSerializer, self).create(validated_data) 
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','username','phone','address']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields=['id','source','destination','bus_no','user','date']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields=['id','ticket','price','mode']

  
