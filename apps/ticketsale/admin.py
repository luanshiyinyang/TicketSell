from django.contrib import admin
from apps.ticketsale.models import Tickets, Users

admin.site.register(Users)
admin.site.register(Tickets)
