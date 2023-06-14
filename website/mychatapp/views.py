from django.shortcuts import render, redirect
from .models import Message, Profile, Friend , Image
from .forms import MessageForm , ImageForm
from django.http import JsonResponse
from django.contrib import messages
import json
import numpy as np
import os

import website.image_detector as image_detector
import website.comment_toxicity_detector as toxicity_detector 



#home
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    form = MessageForm()
    context = {"user": user, "friends": friends , "form":form}
    return render(request, "mychatapp/index.html", context)



#chatting

def detail(request,pk):
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    chats = Message.objects.all()
    rec_chats = Message.objects.filter(msg_sender = profile , msg_reciver = user)
    rec_chats.update(seen=True)
    form = MessageForm()

    if request.method == "POST":
        img=ImageForm(data=request.POST,files=request.FILES)
        if img.is_valid():
            obj=img.instance
            
            file_path = f'static{obj.image.url}'
            file_path = os.path.abspath(file_path)
            result_nudity = image_detector.classify_nudity_image(file_path) # Making prediction and return  boolean if nudity
            print(f"Result of nudity: {result_nudity}")

            image = img.save(commit=False)
            image.img_sender = user
            image.img_reciver = profile
            image.save()

            result_nudity =  image_detector.classify_nudity_image(file_path) # Making prediction and return  boolean if nudity
            print(f"Result of nudity: {result_nudity}")

            image.nudity=result_nudity
            image.save()

            context = {"friend": friend, "form": form, "user":user, 
            "profile":profile, "chats": chats , "num":rec_chats.count() , "form_img":img , "obj":obj , "nudity": result_nudity}
            return render(request, "mychatapp/detail.html", context)
    else:
        img=ImageForm()
        img_all=Image.objects.all()    
        context = {"friend": friend, "form": form, "user":user, 
                "profile":profile, "chats": chats , "num":rec_chats.count() , "form_img":img , "img_all":img_all }
    return render(request, "mychatapp/detail.html", context)
    

#saving,sending and recieving msg

def sentMessages(request ,pk):
    is_toxicity = False
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    

    # Model prediction   
    input_str = toxicity_detector.encode_text(new_chat) # Text vectorization
    is_toxicity = toxicity_detector.classify_toxicity(input_str) # Making prediction and return boolean
    print(is_toxicity)
    # If is_toxicity, then don't send this message
    if is_toxicity == False:
        new_chat_message = Message.objects.create(body = new_chat , msg_sender = user , msg_reciver = profile , seen=False) 
        return JsonResponse(new_chat_message.body , safe=False)
    #elif result_nudity == True:
    #    return JsonResponse("***This image contains nudity and cannot be sent***" , safe = False)
    else :
        print('error')
        return JsonResponse("***This message has toxicity and cannot be send***" , safe=False)


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