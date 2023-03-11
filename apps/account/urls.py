from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_success/', views.register_success, name='register_success'),
]
