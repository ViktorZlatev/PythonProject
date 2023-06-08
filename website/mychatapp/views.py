from django.shortcuts import render, redirect
from .models import Message, Profile, Friend , Image
from .forms import MessageForm , ImageForm
from django.http import JsonResponse
import json
import tensorflow as tf
import numpy as np
import pandas as pd
import os



from tensorflow.keras.layers import TextVectorization
from website.image_detector import *


TOXICITY_FLAG = 0.65

# Loading tensorflow model and preprocessing data
model = tf.keras.models.load_model('../model_comment_toxicity_2.h5', compile=False)

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

    if request.method == "POST":
        img=ImageForm(data=request.POST,files=request.FILES)
        if img.is_valid():
            obj=img.instance
            
            # with open(obj.image.url) as f:
            #     data = f.read()
            
            # obj.image.save('imgfilename.jpg', ContentFile(data))
            # print("Saved image")
            # print(PROJECT_ROOT)
            
            # image_name = obj.image.url.split('/')[-1]
            # base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # full_file_path = os.path.join(base_directory, image_name)
            
            print(f"Our Image url: {obj.image.url}")
            file_path = f'static{obj.image.url}'
            file_path = os.path.abspath(file_path)
            # print(f"Type of obj.image.url: {type(obj.image.url)}")
            print(f"File path: {file_path}")
              
            image = img.save(commit=False)
            image.img_sender = user
            image.img_reciver = profile
            image.save()
            
            result_nudity = classify_nudity_image(file_path)
            print(f"Result of nudity: {result_nudity}")
            
            context = {"friend": friend, "form": form, "user":user, 
                "profile":profile, "chats": chats , "num":rec_chats.count() , "form_img":img , "obj":obj }
            return render(request, "mychatapp/detail.html", context)
    else:
        img=ImageForm()
        image = '0'
    img_all=Image.objects.all()
    context = {"friend": friend, "form": form, "user":user, 
                "profile":profile, "chats": chats , "num":rec_chats.count() , "form_img":img , "img_all":img_all}
    return render(request, "mychatapp/detail.html", context)



#adding_friends

def friends(request):
    user = request.user.profile
    #all_friends = user.friends.all()
    users = Profile.objects.all()
    arr = []
    #for friend in all_friends:
     #   if friend not in users:
      #      arr.append(friend)
    form = MessageForm()
    context = {"user": user, "form":form , "friends":users }
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
    is_toxicity_arr = [type_toxicity for type_toxicity in res[0] if type_toxicity > TOXICITY_FLAG]
    is_toxicity = True if len(is_toxicity_arr) > 0 else False
    print(is_toxicity)
    # If is_toxicity, then don't send this message
    if is_toxicity == False:
        new_chat_message = Message.objects.create(body = new_chat , msg_sender = user , msg_reciver = profile , seen=False) 
        return JsonResponse(new_chat_message.body , safe=False)
    else : return JsonResponse()


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