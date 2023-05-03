from django.shortcuts import render, redirect
from .models import Message, Profile, Friend
from .forms import MessageForm
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model

import tensorflow as tf
import numpy as np
import pandas as pd

from tensorflow.keras.layers import TextVectorization

# Loading tensorflow model and preprocessing data
model = tf.keras.models.load_model('../model_comment_toxicity.h5', compile=False)

df = pd.read_csv('../comment_toxicity_train.csv')
X = df['comment_text']
y = df[df.columns[2:]].values
MAX_FEATURES = 200000
vectorizer = TextVectorization(max_tokens=MAX_FEATURES, output_sequence_length=1800, output_mode='int')
vectorizer.adapt(X.values)


# Create your views here.


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
    
    context = {"friend": friend, "form": form, "user":user, 
               "profile":profile, "chats": chats , "num":rec_chats.count()}
    return render(request, "mychatapp/detail.html", context)



#adding_friends

def friends(request):
    user = request.user.profile
    friends = user.friends.all()
    friends = get_user_model()
    all_friends = friends.objects.all()
    form = MessageForm()
    context = {"user": user, "friends": all_friends , "form":form}
    return render(request, "mychatapp/friends.html" , context)



#saving,sending and recieving msg

def sentMessages(request ,pk):
    is_toxicity = False
    friend = Friend.objects.get(friend_profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.friend_profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    
    # Model prediction   
    input_str = vectorizer(new_chat)
    res = model.predict(np.expand_dims(input_str, 0))
    is_toxicity = [type_toxicity for type_toxicity in df.columns[2:] if res[0][df.columns.get_loc(type_toxicity)] > 0.5]
    
    print(is_toxicity)
    
    
    
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