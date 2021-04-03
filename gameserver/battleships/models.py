from django.db import models

from django.contrib.auth.models import User

class Player(models.Model):
    # created a one to one with the built-in User model
    player = models.OneToOneField(User, related_name='player', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['nickname']


class Game(models.Model):
    # In theory we could let the player choose the size of
    # the game (max_x, max_y) and there could also be multiple players
    name = models.CharField(max_length=50, unique=True)
    maximum_x = models.IntegerField(default=8)
    maximum_y = models.IntegerField(default=8)
    ships_per_person = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(Player)

class Coords(models.Model):
    # Table to save coords for the ships and fire(s)
    x = models.IntegerField()
    y = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Ship(models.Model):
    ship_type = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    coords = models.ManyToManyField(Coords)   

    def __str__(self):
        return self.ship_type

    class Meta:
        ordering = ['ship_type']


class Fire(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result

    class Meta:
        ordering = ['created_at']