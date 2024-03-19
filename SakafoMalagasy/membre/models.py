
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Photo(models.Model):
    fichier = models.ImageField(upload_to='static/image_recette')


class Recette(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)


class Ingredient(models.Model):
    nom = models.CharField(max_length=50)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Etape(models.Model):
    numero = models.PositiveIntegerField()
    description = models.TextField()
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Commentaire(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)





class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    recettes = models.ManyToManyField(Recette)


class Favoris(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    recette = models.ManyToManyField(Recette)

    #pour afficher dans l'administration
    def __str__(self):
        return self.utilisateur.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images', default='default.jpg', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Recette_a_faire(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Recette_effectue(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)