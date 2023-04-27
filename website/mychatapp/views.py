from django.shortcuts import render, redirect
from .models import Message, Profile, Friend
from .forms import MessageForm
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    form = MessageForm()
    context = {"user": user, "friends": friends , "form":form}
    return render(request, "mychatapp/index.html", context)


def detail(request,pk):
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    chats = Message.objects.all()
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_reciver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user":user, 
               "profile":profile, "chats": chats}
    return render(request, "mychatapp/detail.html", context)