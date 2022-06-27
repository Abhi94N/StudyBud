from django.shortcuts import render, redirect

#Query module
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
# register view
# from django.contrib.auth.models import User
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        # check if user exists
        try:
            #fetch username
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        #if user exists authenticates
        user = authenticate(request, email=email, password=password)

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
    form = MyUserCreationForm()
    context = {'form': form}
    
    #on post submit
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    topics = Topic.objects.all()[0:5]
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
    topics = Topic.objects.all()
    if request.method == 'POST':

        # fetch topic to add when creating room
        topic_name = request.POST.get('topic')
        # get or create returns back an object or creates it in model if it doesn't exist, created will let you know whether the object exists or not
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect("home")
    context = {'form': form, 'topics': topics}
    
    return render(request, 'base/room_form.html', context)
@login_required(login_url='login')
def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    
    # instance of form that is prefilled
    form = RoomForm(instance=room)
    
    #get topics
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        # fetch topic to add when creating room
        topic_name = request.POST.get('topic')
        # get or create returns back an object or creates it in model if it doesn't exist, created will let you know whether the object exists or not
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #replace the instance that was fetched
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save
        return redirect('home')
        
        
    
    context = {'form': form, 'topics': topics, 'room': room}
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


#Profile view
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    # pass tine instance of form
    form = UserForm(instance=request.user)
    
    if request.method == 'POST':
        #update form with request files in order to add requests
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form }
    return render(request, 'base/update-user.html', context)
    
#topics
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    content = {"room_messages": room_messages}
    return render(request, 'base/activity.html', content)