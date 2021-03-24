from django.contrib import admin
from Client.models import Profile
from Client.models import Ticket
from Client.models import Payment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Ticket)
admin.site.register(Payment)