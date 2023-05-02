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
    rec_chats = Message.objects.filter(msg_sender = profile , msg_reciver = user)
    rec_chats.update(seen=True)
    form = MessageForm()
    
    context = {"friend": friend, "form": form, "user":user, 
               "profile":profile, "chats": chats , "num":rec_chats.count()}
    return render(request, "mychatapp/detail.html", context)


def sentMessages(request ,pk):
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = Message.objects.create(body = new_chat , msg_sender = user , msg_reciver = profile , seen=False) 
    return JsonResponse(new_chat_message.body , safe=False)


def recivedMessages( request , pk ):
    arr = []
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    chats = Message.objects.filter(msg_sender = profile , msg_reciver = user)
    for chat in chats:
        arr.append(chat.body) 
    return JsonResponse(arr , safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = Message.objects.filter(msg_sender__id=friend.friend_profile.id, msg_reciver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)