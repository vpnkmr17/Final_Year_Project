from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,phone,is_active=True,address=None,date_of_birth=None,password=None):
        if not email:
            raise ValueError("Enter your email please!")
        if not username:
            raise ValueError("Users must have an username!")
        if not phone:
            raise ValueError("Please Enter your mobile number!")
        user=self.model(
			email=self.normalize_email(email),
			username=username,
            phone=phone,
            is_active=True,
            address=address,
            date_of_birth=date_of_birth,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password,phone=None):
        user=self.create_user(email=self.normalize_email(email),
			password=password,
			username=username,
            phone=phone)
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Profile(AbstractBaseUser):
    email=models.EmailField(verbose_name='email',max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=300,blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    data_joined=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    #Add your additional fields
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone'] #You can use additional fields
    objects=MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


class Payment(models.Model):
    price=models.IntegerField()
    mode=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    user=models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE,related_name="tick_user")
    Payment=models.OneToOneField(Payment,null=True,blank=True,on_delete=models.CASCADE,related_name="payment")
    source=models.CharField(max_length=250)
    destination=models.CharField(max_length=250)
    bus_no=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.source)+"---"+str(self.destination)































