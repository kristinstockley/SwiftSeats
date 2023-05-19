from django import forms
from .models import Concert

class CreateConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'artist', 'date', 'venue']


class EditConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'artist', 'date', 'venue']