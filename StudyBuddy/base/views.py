from django.shortcuts import render
from .models import Room
from django.shortcuts import get_object_or_404

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python'}, 
#     {'id':2, 'name':'Design with me'}, 
#     {'id':3, 'name':'Backend developers'}, 
# ]

  


def home(request):
    rooms = Room.objects.all()  # querying from the database for multiple objects
    context ={'rooms': rooms}
    return render( request, 'base/home.html', context)




def room(request, pk):
    # room = get_object_or_404(Room, id=pk)  # querying from the database for single object
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


# def room(request, pk):
#     rooms = Room.objects.all()
#     room = None
#     for i in rooms:
#         if i.ID == int(pk):
#             room = i
#     context = {'room': room}
#     return render( request, 'base/room.html', context)