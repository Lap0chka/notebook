from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # Login & Log out
    path('login/', views.CustomLoginView.as_view(), name='login',),
    path('logout/', views.logout_user, name='logout',),

    # Profile
    path('profile/', views.profile, name='profile',),
]
