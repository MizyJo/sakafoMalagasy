from django.contrib.auth import logout
from django.shortcuts import render, redirect

from membre.models import Recette, Photo, Etape, Ingredient


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        recette = Recette.objects.all()
        return render(request, "membre/index.html",{'recette': recette})
    else:
        return redirect('index')


def logouts(request):
    logout(request)
    return redirect('index')


def ajout_recette(request):
    if request.user.is_authenticated:
        return render(request, 'membre/ajout_recette.html')
    else:
        return redirect('/')


def add_recette(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            etapes = request.POST.getlist('step[]')
            ingrediants = request.POST.getlist('ingredient[]')
            titre = request.POST.get('titre')
            description = request.POST.get('description')
            photo = request.FILES.get('image')
            e = 1
            i = 1
            print(etapes)
            print(ingrediants)
            print(photo)
            if photo and titre != "" and description != "" and etapes and ingrediants:
                image = Photo.objects.create(fichier=photo)
                recette = Recette.objects.create(titre=titre, description=description, auteur=request.user, photo=image)
                for etape in etapes:
                    Etape.objects.create(numero=e, description=etape, recette=recette)
                    e = e+1
                for ingrediant in ingrediants:
                    Ingredient.objects.create(nom=ingrediant, recette=recette)
                success_message = "Recette ajouté avec sucès"
                return render(request,'membre/ajout_recette.html',{'success_message': success_message})
            else:
                success_message = "Tous les champs sont obligatoire"
                return render(request, 'membre/ajout_recette.html', {'error_message': success_message})
        else:
            return redirect('/membre')
    else:
        return redirect("/")



