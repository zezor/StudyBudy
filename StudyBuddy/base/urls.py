
from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),
    path('create_room/', views.createRoom, name="create_room"),

]
