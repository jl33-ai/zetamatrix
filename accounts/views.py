from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render, HttpResponse
from .models import PlayerStats
from game.models import GameSession
from django.db.models import Avg, StdDev, Func, F
from django.db.models.functions import TruncDay


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LogoutView(generic.CreateView):
    template_name = 'registration/logout.html'

def profile(request):
    player_stats, created = PlayerStats.objects.get_or_create(
        user=request.user,
        defaults={
            'games_played': 0,
            'questions_answered': 0,
            'has_world_record': False,
            'has_come_top_50_daily_challenge': False
        }
    )
    game_sessions_stats = GameSession.objects.filter(user=request.user, length=120)\
                                         .aggregate(e_of_x=Avg('score'), sd=StdDev('score'))

    game_session_data = GameSession.objects.filter(user=request.user, length=120)\
                                        .annotate(date=TruncDay('start_time'))\
                                        .values('date')\
                                        .annotate(average_score=Avg('score'))\
                                        .order_by('date')
    
    skill_dict = {
        ''
    }

    skill_level = game_sessions_stats['e_of_x']
    
    payload = {
        'games_played': player_stats.games_played,
        'questions_completed': player_stats.questions_answered,
        'has_world_record': player_stats.has_world_record,
        'e_of_x': round(game_sessions_stats['e_of_x'], 1) if game_sessions_stats['e_of_x'] is not None else 0,
        'sd': round(game_sessions_stats['sd'], 1) if game_sessions_stats['sd'] is not None else 0,
        'x_progress_data' : [item['date'].isoformat() for item in game_session_data],
        'y_progress_data' : [item['average_score'] for item in game_session_data]
    }

    return render(request, 'profile.html', context=payload)