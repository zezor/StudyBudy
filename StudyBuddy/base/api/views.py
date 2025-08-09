from django.http import JsonResponse
from rest_framework import serializers

def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/<id>',
            
            ]
    
    return JsonResponse(routes, safe=False)
    