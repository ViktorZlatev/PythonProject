from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name = "index"),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('friends' , views.friends , name="friends"),
    path('sent_msg/<str:pk>' , views.sentMessages , name="sent_msg"),
    path('rec_msg/<str:pk>', views.recivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification ,  name = "notification"),

]