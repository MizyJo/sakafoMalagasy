
from django.urls import path
from membre.views import index, logouts, ajout_recette, add_recette, profile, add_profil, recette, get_etape, \
    get_ingredient, get_recette, add_etape, add_ingredient

urlpatterns = [

    path('', index, name="accueil"),
    path('logout', logouts, name="logout"),
    path('ajout_recette', ajout_recette, name="ajout_recette"),
    path('add_recette', add_recette, name="add_recette"),
    path('profile', profile, name="profile"),
    path('ajout_photo_profil', add_profil, name="ajout_photo_profil"),
    path('recette', recette, name="recette"),
    path('get_etape/<int:recette_id>', get_etape, name="get_etape"),
    path('get_ingredient/<int:recette_id>', get_ingredient, name="get_ingredient"),
    path('get_recette/<int:recette_id>', get_recette, name="get_recette"),
    path('add_etape', add_etape, name="add_etape"),
    path('add_ingredient', add_ingredient, name="add_ingredient"),

]