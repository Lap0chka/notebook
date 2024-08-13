
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # Login & Log out
    path('login/', views.CustomLoginView.as_view(), name='login',),
]
