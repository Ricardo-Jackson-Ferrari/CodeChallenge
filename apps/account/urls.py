from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path(
        'active_account/<uidb4>/<token>',
        views.active_account,
        name='active_account',
    ),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
