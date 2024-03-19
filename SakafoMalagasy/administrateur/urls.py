from django.urls import path
from administrateur.views import index, dashboard, login_admin

urlpatterns = [
    path('', index, name='index'),
    path('login', login_admin, name='login_admin'),
    path('dashboard', dashboard, name='dashboard'),


]