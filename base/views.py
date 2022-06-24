from django.shortcuts import render, redirect

#Query module
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
# register view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm

#Django has messages
from django.contrib import messages
#views that require login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

#create your registration and login views here
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        # check if user exists
        try:
            #fetch username
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        #if user exists authenticates
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # adds session in database and in browser
            login(request, user)
            # return home
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist')
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # do not need page because it is default value
    form = UserCreationForm()
    context = {'form': form}
    
    #on post submit
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #don't commit until its clean
            user = form.save(commit=False)
            
            user.username = user.username.lower()
            user.save()
            # once save login
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            
    
    return render(request, 'base/login_register.html',context)

# Create your app views here.
def home(request):
    # pass tp query
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # icontains - filters by string passed if string matches - 
    # the object and param and function need double underscore topic__name__incontains = room.topic.icontains
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    # Room based search filter
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    #flash message use object message so we will specify parent object and message
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        
        #when user comments, they are added
        room.participants.add(request.user)
        #redirect to same room
        return redirect('room', pk=room.id)
    
    context = context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        # Fetches data from request to form
        form = RoomForm(request.POST)
        if form.is_valid():
            
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            #return to page based on name
            return redirect("home")
    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)
@login_required(login_url='login')
def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    
    # instance of form that is prefilled
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        #replace the instance that was fetched
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
        
        
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    #check if user is owner of room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

#CHAT ROOM message Crud
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room_id = Room.objects.get(name=message.room).id
    #check if user is owner of room
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('room',pk=room_id)
    return render(request, 'base/delete.html', {'obj': message})
    