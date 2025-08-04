from django.shortcuts import render, redirect
from .models import Room, Topic
from django.shortcuts import get_object_or_404
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python'}, 
#     {'id':2, 'name':'Design with me'}, 
#     {'id':3, 'name':'Backend developers'}, 
# ]

  


def home(request):
    # rooms = Room.objects.all()  # querying from the database for multiple objects
    rooms = Room.objects.filter()  # filter from the database for selected objects
    topics = Topic.objects.all()
    context ={'rooms': rooms, 'topics':topics}
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


def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
         room.delete()
         return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})