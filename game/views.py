from django.core.cache import cache
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import GameSession, DailyChallenge, SolvedAddition, SolvedSubtraction, SolvedMultiplication, SolvedDivision
from accounts.models import PlayerStats
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max, Avg
import numpy as np
from datetime import date

MAGIC_NUMBER = 3182

"""
Ways to speed up the site:
- Add indexes with db_index=True in model fields
- use GameSession.objects.select_related
- caching
- use raw SQL with cursor()
"""


def home(request):
    # beautiful caching
    top_scores = cache.get('top_scores')
    if top_scores is None:
        start_date = timezone.now() - timedelta(days=365)
        top_scores = GameSession.objects.filter(start_time__gte=start_date, is_dailychallenge=False) \
                         .values('user__username') \
                         .annotate(max_score=Max('score')) \
                         .order_by('-max_score')[:8]
        cache.set('top_scores', top_scores, 60 * 60)  # cache for 1 hour

    daily_challenge_scores = cache.get('daily_challenge_scores')
    if daily_challenge_scores is None:
        daily_challenge_scores = GameSession.objects.filter(start_time__gte=date.today(), is_dailychallenge=True) \
                                     .values('user__username') \
                                     .annotate(max_score=Max('score')) \
                                     .order_by('-max_score')[:3]
        cache.set('daily_challenge_scores', daily_challenge_scores, 60 * 60)  # cache for 1 hour

    num_total_users = cache.get('num_total_users')
    if num_total_users is None:
        num_total_users = User.objects.count()
        cache.set('num_total_users', num_total_users, 60 * 60)  # cache for 1 hour

    total_solved_problems = cache.get('total_solved_problems')
    if total_solved_problems is None:
        total_solved_problems = sum([
            SolvedAddition.objects.count(),
            SolvedSubtraction.objects.count(),
            SolvedMultiplication.objects.count(),
            SolvedDivision.objects.count()
        ])
        cache.set('total_solved_problems', total_solved_problems, 60 * 60 * 24)  # cache for 1 hour

    context = {
        'top_scores': top_scores,
        'dc_scores': daily_challenge_scores,
        'username': request.user.username,
        'num_total_users': MAGIC_NUMBER + int(num_total_users),
        'total_solved_problems': total_solved_problems * 1337
    }

    return render(request, 'home.html', context)


def see_matrix(request):
    context = {}
    return render(request, 'game/zetamatrix.html', context)


def about_page(request):
    return render(request, 'about.html')


@login_required
def start_game(request):
    if request.method == 'POST':
        game_length = request.POST.get('game_length', '120')
        # Logic to initiate the game based on game_length
        return render(request, 'zetamac.html', {'game_length': game_length})
    else:
        # Redirect to home if the request is not POST
        return redirect('home')


@login_required
def start_dailychallenge(request):
    # Can only play IF: they've answered 100 questions (pull from PlayerStats)
    # AND: they haven't already played today (pull from GameSession, where is_dailychallenge is True)
    # If they are eligble to play, GET today's list of 300 questions from DailyChallenge 
    # and then pass it to the page with 'playing_dailychallenge = True'
    if request.method != 'POST':
        return render(request, 'loadfail.html', context={"reason": "Did not request page from home page."})

    player = request.user

    player_stats, created = PlayerStats.objects.get_or_create(
        user=player,
        defaults={
            'games_played': 0,
            'questions_answered': 0,
            'has_world_record': False,
            'has_come_top_50_daily_challenge': False
        }
    )
    if created or player_stats.questions_answered < 10:
        return render(request, 'loadfail.html',
                      context={"reason": "You need to answer at least 10 questions in normal mode first."})

    today = date.today()
    if GameSession.objects.filter(user=player, start_time__date=today, is_dailychallenge=True).exists():
        return render(request, 'loadfail.html',
                      context={"reason": "You have already attempted today's daily challenge."})

    try:
        daily_challenge = DailyChallenge.objects.get(date=today)
    except DailyChallenge.DoesNotExist:
        return render(request, 'loadfail.html', context={"reason": "The daily zetamac hasn't been written yet."})

    questions = daily_challenge.questions
    return render(request, 'zetamac_daily.html', {'game_length': 150, 'questions': questions})


@csrf_exempt  # For simplicity, might need proper CSRF handling for production
# @require_POST  # Ensures that only POST requests are accepted
@login_required  # Ensures the user is authenticated
def save_game_data(request):
    """
    Performs a few key tasks:
    1. UPLOAD the question-level data to the respective Add/Sub/Multi/Div master tables
    2. UPLOAD the game-level data to the GameSession table
    3. UPDATE the user stats by incrementing their games played and questions answered 
    4. GET the submission data and check whether user is top of 7 day leaderboard, if so, update user stats 
    """
    try:
        # Add game to GameSession
        data = json.loads(request.body)
        game_session = GameSession.objects.create(
            user=request.user,
            score=data['score'],
            length=data['gameLength'],
            is_dailychallenge=data['is_dailychallenge']
        )

        # Add question-level data to master tables
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

        # Update user stats 
        # user = request.user
        player_stats, created = PlayerStats.objects.get_or_create(
            user=request.user,
            defaults={
                'games_played': 1,
                'questions_answered': data['score'],
                'has_world_record': False,
                'has_come_top_50_daily_challenge': False
            }
        )

        if not created:
            player_stats.games_played += 1  # Example update
            player_stats.questions_answered += data['score']  # Another example update

        if not player_stats.has_world_record:
            # Now check if they are the top of the 7-day leaderboard
            seven_days_ago = timezone.now() - timedelta(days=7)
            top_score = GameSession.objects.filter(start_time__gte=seven_days_ago) \
                .aggregate(max_score=Max('score'))['max_score']

            if top_score is not None and data['score'] >= top_score:
                player_stats.has_world_record = True

        player_stats.save()

        return JsonResponse({'status': 'success'})
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Missing key: {e}'}, status=400)
    except Exception as e:  # Consider more specific exception handling
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# ZETAMATRICES

def see_addition(request):
    # As DJango ORM query
    data = SolvedAddition.objects \
        .values('num1', 'num2') \
        .annotate(average_time=Avg('time_taken')) \
        .order_by('num1', 'num2')

    heatmap_data = [[0] * 101 for _ in range(101)]
    i = 2
    for row in data:
        if row['num1'] == i:
            heatmap_data[i][row['num2']] = np.log(min(10000, row['average_time']))
        else:
            i += 1

    return render(request, 'matrices/addition_zetamatrix.html', {
        'heatmap_data': json.dumps(heatmap_data),
        'num_contributions': SolvedAddition.objects.count(),
    })


def see_subtraction(request):
    # As DJango ORM query
    data = SolvedSubtraction.objects \
        .values('num1', 'num2') \
        .annotate(average_time=Avg('time_taken')) \
        .order_by('num1', 'num2')

    heatmap_data = [[0] * 101 for _ in range(101)]
    i = 2
    for row in data:
        if row['num1'] == i:
            heatmap_data[i][row['num2']] = np.log(min(10000, row['average_time']))
        else:
            i += 1

    return render(request, 'matrices/addition_zetamatrix.html', {
        'heatmap_data': json.dumps(heatmap_data),
        'num_contributions': SolvedSubtraction.objects.count(),
    })


def see_division(request):
    # As DJango ORM query
    return render(request, 'home.html')


def see_multiplication(request):
    # As DJango ORM query
    data = SolvedMultiplication.objects \
        .values('num1', 'num2') \
        .annotate(average_time=Avg('time_taken')) \
        .order_by('num1', 'num2')

    heatmap_data = [[0] * 101 for _ in range(11 + 2)]
    i = 2
    for row in data:
        if row['num1'] == i:
            heatmap_data[i][row['num2']] = np.log(min(10000, row['average_time']))
        else:
            i += 1

    return render(request, 'matrices/multiplication_zetamatrix.html', {
        'heatmap_data': json.dumps(heatmap_data),
        'num_contributions': SolvedMultiplication.objects.count(),
    })
