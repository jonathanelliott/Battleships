from django.contrib import admin

from .models import Player
from .models import Game
from .models import Coords
from .models import Ship
from .models import Fire

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Coords)
admin.site.register(Ship)
admin.site.register(Fire)
