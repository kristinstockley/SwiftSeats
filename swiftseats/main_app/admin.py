from django.contrib import admin
from .models import Ticket, Concert, Photo

admin.site.register(Ticket)
admin.site.register(Concert)
admin.site.register(Photo)
