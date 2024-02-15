from django.urls import path
from . import views


urlpatterns = [
    path('', views.workspace),
    path('login', views.login),
    path('logout', views.logout),
    path('add_row/', views.add_row, name='add_row'),
    path('delete_row/', views.delete_row, name='delete_row'),
    path('textarea_view/', views.textarea_view, name='textarea_view'),
    path('save/', views.save_data, name='save_data'),
    path('share', views.share, name='share'),
    path('send_share/', views.send_share, name='send_share'),
    path('save_share/', views.save_share, name='save_share'),
    path('download_file/', views.download_file, name='download_file'),
    # path('update_content', views.update_content, name='update_content'),
    path('auto_save', views.auto_save, name='auto_save'),
    path('upload_file', views.upload_file, name='upload_file'),
]
