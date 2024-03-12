from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('checkin/', views.checkin, name='checkin'),
    path('checkout/', views.checkout, name='checkout'),
    path('lunchbreak/', views.lunchbreak, name='lunchbreak'),
    path('employee/<int:id>/log/', views.employeelog, name='employeelog'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),
]