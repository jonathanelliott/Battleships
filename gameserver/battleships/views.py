from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Player, Game
from .forms import CreateGame

def frontpage(request):    

    return render(request, 'battleships/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            user.email = user.username
            user.save()

            player = Player.objects.create(player=user)
            player.save()

            login(request, user)
            
            return redirect('dashboard')
    else:
         form = UserCreationForm()

    return render(request, 'battleships/signup.html', {'form': form})

@login_required
def dashboard(request):

    if request.method == 'POST':
        form = CreateGame(request.POST)

        if form.is_valid():
            
            maximum_x = int(request.POST.get('maximum_x'))
            maximum_y = int(request.POST.get('maximum_y'))
            game_name = request.POST.get('name')
            # just a solo game for now         
            game = Game.objects.create(name=game_name, maximum_x=maximum_x, maximum_y=maximum_y, created_by=request.user)
            game.save()

            # this next part is a bit artificial as we are getting the values from
            # the db to create the game to check it works but we could just get them directly
            # from the request obj
            test_game = Game.objects.get(name=game_name)

            # now we need to populate the game with ships - randomly first

            grid = [[None] * test_game.maximum_x for i in range(test_game.maximum_y)]
             
            context = {
                'grid': grid,
                'xrange': range(0, test_game.maximum_x),
                'yrange': range(0, test_game.maximum_y),
                'form': form,
            }
            return render(request, 'battleships/dashboard.html', context)  
    else:
        form = CreateGame()
        grid = [[None] * 7 for i in range(7)]

        context = {
            'grid': grid,
            'xrange': range(0, 7),
            'yrange': range(0, 7),
            'form': form,
        }
    return render(request, 'battleships/dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)

    return redirect('frontpage')


