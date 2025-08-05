from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import RoomForm

# Create your views here.
## Login, Register, Logout Views
def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').strip().lower()  # Normalize username to lowercase
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exit please register')
        user = authenticate(request , username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password does not exit please try again')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

## Login, Register, Logout Views
def logoutUser(request):
    logout(request)
    return redirect('login')

## Login, Register, Logout Views
def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # Normalize username to lowercase
            user.save()
            login(request, user) # Automatically log in the user after registration
            messages.success(request, 'Registration successful')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})
    

    # Uncomment the following lines if you want to implement registration functionality
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    # if request.method == "POST":
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     password2 = request.POST.get('password2')
        
    #     if password != password2:
    #         messages.error(request, 'Passwords do not match')
    #     else:
    #         user = User.objects.create_user(username=username, email=email, password=password)
    #         user.save()
    #         login(request, user)
    #         return redirect('home')
    
    # context = {'page': page}
    # return render(request, 'base/login_register.html', context)

 



def home(request):
    # rooms = Room.objects.all()  # querying from the database for multiple objects
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                                Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q) 
                                )# filter from the database for selected objects
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context ={'rooms': rooms, 'topics':topics, 'room_count': room_count}
    return render( request, 'base/home.html', context)




def room(request, pk):
    # room = get_object_or_404(Room, id=pk)  # querying from the database for single object
    room = Room.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('-created')  # Get all messages related to the room and order them by creation date
    participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You do not have permission to perform this action!!')


    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You do not have permission to perform this action!!')
    
    if request.method == 'POST':
         room.delete()
         return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})