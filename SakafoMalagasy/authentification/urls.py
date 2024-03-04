from django.urls import path
from authentification.views import register, save_user, vue_login, tchek_login

urlpatterns = [
    path('register', register, name="register"),
    path('save_user',save_user,name='save_user'),
    path('login',vue_login,name='login'),
    path('tchek_login',tchek_login,name='tchek_login'),
]