from django.contrib import admin
from .models import *

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'updated', 'created')

admin.site.register(Room, RoomAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Topic,  TopicAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display =('id', 'room', 'body', 'updated', 'created')

admin.site.register(Message, MessageAdmin)