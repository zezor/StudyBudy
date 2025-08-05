from django import forms
from django.forms  import ModelForm
from .models import Room , Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }