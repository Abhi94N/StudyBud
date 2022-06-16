from django.shortcuts import render, redirect

#Query module
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm



# Create your views here.
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
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        # Fetches data from request to form
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            #return to page based on name
            return redirect("home")
    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    
    # instance of form that is prefilled
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        #replace the instance that was fetched
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
        
        
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
    