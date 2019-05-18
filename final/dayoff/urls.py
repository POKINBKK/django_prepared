from django.urls import path
from dayoff import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.mylogin, name='mylogin'),
    path('register/', views.register, name='register'),
    path('request/', views.leaveRequest, name='request'),
]