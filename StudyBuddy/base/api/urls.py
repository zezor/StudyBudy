from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes),
    path('api/rooms', views.getRoutes, name='get-routes'),
    path('api/rooms/<int:id>', views.getRoom, name='get-room'),
]
