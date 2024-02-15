from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='authorization/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authorization/logout.html'), name='logout'),
    path('', views.index, name='index')
]



