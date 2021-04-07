from django.forms import ModelForm

from .models import Game

class CreateGame(ModelForm): 
    class Meta:
        model = Game
        fields = ['name', 'maximum_x', 'maximum_y', 'ships_per_person']

        