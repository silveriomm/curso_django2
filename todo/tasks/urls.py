from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.helloworld),
    path('', views.taskList, name='taskList'),
    path('yourname/<str:name>', views.yourName, name='your-name'),
]