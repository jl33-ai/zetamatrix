from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
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


@login_required
def profile(request):
    # Get or create player stats
    player_stats, _ = PlayerStats.objects.get_or_create(
        user=request.user,
        defaults={
            'games_played': 0,
            'questions_answered': 0,
            'has_world_record': False,
            'has_come_top_50_daily_challenge': False
        }
    )

    # Cache and retrieve game sessions stats
    player_stats_cache_key = f'game_sessions_stats_{request.user.id}'
    game_sessions_stats = cache.get(player_stats_cache_key)
    if game_sessions_stats is None:
        game_sessions_stats = GameSession.objects.filter(user=request.user, length=120) \
            .aggregate(e_of_x=Avg('score'), sd=StdDev('score'))
        cache.set(player_stats_cache_key, game_sessions_stats, 60 * 5)  # Cache for 5 minutes

    # Cache and retrieve game session data
    game_session_data_cache_key = f'game_session_data_{request.user.id}'
    game_session_data = cache.get(game_session_data_cache_key)
    if game_session_data is None:
        game_session_data = list(GameSession.objects.filter(user=request.user, length=120)
                                 .annotate(date=TruncDay('start_time'))
                                 .values('date')
                                 .annotate(average_score=Avg('score'))
                                 .order_by('date'))
        cache.set(game_session_data_cache_key, game_session_data, 60 * 5)  # Cache for 5 minutes

    payload = {
        'games_played': player_stats.games_played,
        'questions_completed': player_stats.questions_answered,
        'has_world_record': player_stats.has_world_record,
        'e_of_x': round(game_sessions_stats['e_of_x'] or 0, 1),
        'sd': round(game_sessions_stats['sd'] or 0, 1),
        'x_progress_data': [item['date'].isoformat() for item in game_session_data],
        'y_progress_data': [item['average_score'] for item in game_session_data]
    }

    return render(request, 'profile.html', context=payload)
