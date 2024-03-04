from django.urls import path
from membre.views import index, logouts

urlpatterns = [
    path('', index, name="accueil"),
    path('logout',logouts,name="logout"),
]