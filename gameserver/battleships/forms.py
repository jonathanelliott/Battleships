from django import forms

from .models import Game

class CreateGrid(forms.Form): 
    maximum_x = forms.IntegerField(label='X', max_value=101)
    maximum_y = forms.IntegerField(label='Y', max_value=101)


        