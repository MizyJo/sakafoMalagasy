from django.urls import path
from membre.views import index, logouts, ajout_recette, add_recette

urlpatterns = [
    path('', index, name="accueil"),
    path('logout',logouts,name="logout"),
    path('ajout_recette',ajout_recette,name="ajout_recette"),
    path('add_recette', add_recette, name="add_recette"),
]