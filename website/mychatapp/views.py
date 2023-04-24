from django.shortcuts import render
from .models import Profile , Friend

# Create your views here.
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user":user , "friends":friends}
    return render(request , "mychatapp/index.html" , context)

def detail(request , pk):
    friend = Friend.objects.get(friend_profile_id = pk)
    context = {'friend':friend}
    return render(request , "mychatapp/detail.html" , context)
