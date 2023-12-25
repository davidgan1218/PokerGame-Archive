from django import forms
from .models import Player


class BetForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['bet']
