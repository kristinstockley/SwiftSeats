from django.contrib import admin
from .models import Ticket, Concert

admin.site.register(Ticket)
admin.site.register(Concert)