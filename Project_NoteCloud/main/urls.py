from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('developers', views.developers),
    path('installation', views.installation),
    path('login', views.login),
]
