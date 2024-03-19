
from django.urls import path
from membre.views import index, logouts, ajout_recette, add_recette, profile, add_profil, recette, add_favoris, \
    get_etape, remove_favoris, \
    get_ingredient, get_recette, add_etape, add_ingredient, get_etape_by_id, get_ingredient_by_id, edit_etape, \
    edit_ingredient, delete_recette, delete_etape, delete_ingredient, edit_recette, affiche_recette, recette_a_faire, \
    liste_raf, recette_effectue, liste_re

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
    path('add_favoris/<int:recette_id>', add_favoris, name="add_favoris"),
    path('add_favoris/', add_favoris, name='add_favoris_all'),
    path('add_etape', add_etape, name="add_etape"),
    path('remove_favoris/<int:recette_id>/', remove_favoris, name='remove_favoris'),
    path('add_ingredient', add_ingredient, name="add_ingredient"),
    path('get_etape_by_id/<int:etape_id>', get_etape_by_id, name="get_etape_by_id"),
    path('get_ingredient_by_id/<int:ingredient_id>', get_ingredient_by_id, name=""),
    path('edit_etape', edit_etape, name="edit_etape"),
    path('edit_ingredient', edit_ingredient, name="edit_ingredient"),
    path('edit_recette', edit_recette, name="edit_recette"),
    path('delete_recette', delete_recette, name="delete_recette"),
    path('delete_etape', delete_etape, name="delete_etape"),
    path('delete_ingredient', delete_ingredient, name="delete_ingredient"),
    path('affiche_recette/<int:recette_id>', affiche_recette, name='affiche_recette'),
    path('recette_a_faire/<int:recette_id>', recette_a_faire, name='recette_a_faire'),
    path('recette_a_faire', liste_raf, name='recette_a_faire'),
    path('recette_effectue/<int:recette_id>', recette_effectue, name='recette_effectue'),
    path('recette_effectue', liste_re, name="recette_effectue"),

]