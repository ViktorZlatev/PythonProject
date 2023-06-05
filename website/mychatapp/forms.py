from django import forms
from django.forms import ModelForm
from .models import Message , Image

class MessageForm(ModelForm):
    body = forms.CharField( widget=forms.Textarea(attrs = { 'class':'forms' , 'rows':5 , 'placeholder':'type message here'} ) )
    class Meta:
        model = Message
        fields = ["body"]

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields = ('image' ,)
