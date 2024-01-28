from django.urls import path, include
from .views import SignUpView
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile')
]
