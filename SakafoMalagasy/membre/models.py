
from django.db import models
from django.contrib.auth.models import User


class Recette(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)


class Ingredient(models.Model):
    nom = models.CharField(max_length=50)


class Etape(models.Model):
    numero = models.PositiveIntegerField()
    description = models.TextField()
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Commentaire(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Photo(models.Model):
    fichier = models.ImageField(upload_to='photos/')
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    recettes = models.ManyToManyField(Recette)


class Favoris(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
