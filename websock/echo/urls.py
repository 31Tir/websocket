from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name='index'),
    path('image/', views.echo_image, name='echo_image'),
    path('chat/<str:username>/', views.join_chat, name='join_chat'),
    path('chat/api/<str:username>/', views.api_message, name='join_chat'),
]