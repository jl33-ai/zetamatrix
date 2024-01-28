from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import GameSession, SolvedAddition, SolvedSubtraction, SolvedMultiplication, SolvedDivision
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max, Avg
import numpy as np

# Create your views here.
def home(request):

    # fetch leaderboard
    seven_days_ago = timezone.now()-timedelta(days=7)
    top_scores = GameSession.objects.filter(start_time__gte=seven_days_ago)\
                                     .values('user__username')\
                                     .annotate(max_score=Max('score'))\
                                     .order_by('-max_score')[:10]  # Adjust the number as needed

    context = {
        'top_scores': top_scores,
        'username' : request.user.username,
        }

    if request.user.is_authenticated: 
        context['stats']="Your summary statistics here"
    return render(request, 'home.html', context)

def seematrix(request):
    context = {}
    return render(request, 'game/zetamatrix.html', context)




@login_required
def start_game(request):
    if request.method == 'POST':
        game_length = request.POST.get('game_length')
        # Logic to initiate the game based on game_length
        return render(request, 'zetamac.html', {'game_length': game_length})
    else:
        # Redirect to home if the request is not POST
        return redirect('home')
    
@csrf_exempt  # For simplicity, might need proper CSRF handling for production
#@require_POST  # Ensures that only POST requests are accepted
@login_required  # Ensures the user is authenticated
def save_game_data(request):
    try:
        data = json.loads(request.body)
        game_session = GameSession.objects.create(
            user=request.user,
            score=data['score'],
            length=data['gameLength']
        )

        # Mapping operators to models
        operator_to_model = {
            '+': SolvedAddition,
            '-': SolvedSubtraction,
            '*': SolvedMultiplication,
            '/': SolvedDivision
        }

        for question in data['questionsSolved']:
            model = operator_to_model.get(question['operator'])
            if model:
                model.objects.create(
                    user=request.user,
                    num1=question['num1'],
                    num2=question['num2'],
                    time_taken=question['timeTaken']
                )

        return JsonResponse({'status': 'success'})
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Missing key: {e}'}, status=400)
    except Exception as e:  # Consider more specific exception handling
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def see_addition(request):
    # As DJango ORM query
    data = SolvedAddition.objects \
        .values('num1', 'num2') \
        .annotate(average_time=Avg('time_taken')) \
        .order_by('num1', 'num2')
    
    heatmap_data = [[0]*99 for _ in range(99)]
    i=2
    for row in data:
        if row['num1']==i:
            heatmap_data[i-2][row['num2']-2]=np.log(min(10000, row['average_time']))
        else:
            i+=1

    return render(request, 'addition_zetamatrix.html', {'heatmap_data': json.dumps(heatmap_data)})

def see_multiplication(request):
    # As DJango ORM query
    data = SolvedMultiplication.objects \
        .values('num1', 'num2') \
        .annotate(average_time=Avg('time_taken')) \
        .order_by('num1', 'num2')
    
    heatmap_data = [[0]*99 for _ in range(11)]
    i=2
    for row in data:
        if row['num1']==i:
            heatmap_data[i-2][row['num2']-2]=np.log(min(10000, row['average_time']))
        else:
            i+=1

    return render(request, 'multiplication_zetamatrix.html', {'heatmap_data': json.dumps(heatmap_data)})