from django.urls import path
from administrateur.views import index, dashboard, login_admin, desactive_user, delete_user, liste_recette, last_login

urlpatterns = [
    path('', index, name='index'),
    path('login', login_admin, name='login_admin'),
    path('dashboard', dashboard, name='dashboard'),
    path('desactive_user/<int:id>', desactive_user, name='desactive_user'),
    path('delete_user/<int:user_id>', delete_user, name='delete_user'),
    path('liste_recette', liste_recette, name="liste_reecette"),
    path('last_login', last_login, name='last_login'),
]