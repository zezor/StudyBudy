from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import RoomForm, MessageForm, UserForm

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
    return redirect('home')

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
    # description = room.description
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) | Q(room__name__icontains=q) |
                                           Q(room__description__icontains=q)).order_by('-created')[:5]  # Get the latest 5 messages related to the search query

    context ={'rooms': rooms, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}
    return render( request, 'base/home.html', context)




def room(request, pk):
    # room = get_object_or_404(Room, id=pk)  # querying from the database for single object
    room = Room.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('-created')  # Get all messages related to the room and order them by creation date
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)  # Add the user to the room's participants
        messages.success(request, 'Message sent successfully!')

        return redirect('room', pk=room.id)
    
    participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You do not have permission to perform this action!!')


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)  # Get or create the topic
        room.name = request.POST.get('name')  # Get the room name
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')


    context = {'form':form, 'room': room, 'topics': topics}
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


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You do not have permission to perform this action!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user or request.user != message.room.host:
        return HttpResponse('You do not have permission to perform this action!!')
    return render(request, 'base/message_form.html', {'form': form, 'message': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'An error occurred while updating the profile.')


    return render(request, 'base/update_user.html', {'form': form})