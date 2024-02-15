from django.urls import path
from . import views


urlpatterns = [
    path('mobile_login', views.mobile_login, name='mobile_login'),
    path('get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('get_salt', views.get_salt, name='get_salt'),
    path('get_data', views.get_data, name='get_data'),
    path('save_cloud_note', views.save_cloud_note, name='save_cloud_note'),
]