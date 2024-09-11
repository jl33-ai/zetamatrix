from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("see_addition/", views.see_addition, name='see_addition'),
    path("see_subtraction/", views.see_subtraction, name='see_subtraction'),
    path("see_multiplication/", views.see_multiplication, name='see_multiplication'),
    path("see_division/", views.see_division, name='see_division'),

    
    path("start_game/", views.start_game, name='start_game'),
    path("start_dailychallenge/", views.start_dailychallenge, name='start_dailychallenge'),
    path("save_game_data/", views.save_game_data, name='submit_game_data'),
    path("about/", views.about_page, name='about_page'),
]