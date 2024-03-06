from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from membre.models import Recette, Photo, Etape, Ingredient


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        recette = Recette.objects.all()
        active_page = "explorer"
        return render(request, "membre/index.html",{'recette': recette, 'active_page': active_page})
    else:
        return redirect('index')


def logouts(request):
    logout(request)
    return redirect('index')


def ajout_recette(request):
    if request.user.is_authenticated:
        active_page = "ajout_recette"
        return render(request, 'membre/ajout_recette.html', {'active_page': active_page})
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
                active_page="ajout_recette"
                success_message = "Recette ajouté avec sucès"
                return render(request,'membre/ajout_recette.html',{'active_page': active_page, 'success_message': success_message})
            else:
                active_page = "ajout_recette"
                success_message = "Tous les champs sont obligatoire"
                return render(request, 'membre/ajout_recette.html', {'active_page':active_page, 'error_message': success_message})
        else:
            return redirect('/membre')
    else:
        return redirect("/")


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        active_page="profile"
        return render(request, 'membre/profile.html', {'active_page': active_page, 'user': user})
    else:
        return redirect('/')


def add_profil(request):
    if request.user.is_authenticated:
        active_page = "profile"
        user = request.user
        if request.method == "POST":
            image = request.FILES.get('photo')
            if image:
                request.user.profile.image = image
                request.user.profile.save()
                return render(request, 'membre/profile.html', {'active_page': active_page, 'user': user, 'success_message': 'photo de profil mise a jour'})
            else:
                return render(request, 'membre/profile.html', {'error_message': 'fichier non compatible ou manquant', 'active_page': active_page, 'user': user})

        else:
            return redirect('/membre/profile')


def recette(request):
    if request.user.is_authenticated:
        active_page = "recette"
        recette = Recette.objects.filter(auteur_id=request.user.id)
        return render(request, "membre/recette.html", {'active_page': active_page, 'recette': recette})


def get_etape(request, recette_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            etape = Etape.objects.filter(recette_id = recette_id).values('numero','description')
            return JsonResponse(list(etape), safe=False)
        else:
            return redirect('/membre/')
    else:
        return redirect('/')


def get_ingredient(request, recette_id ):
    if request.user.is_authenticated:
        if request.method == "GET":
            ingredient = Ingredient.objects.filter(recette_id=recette_id).values('nom')
            return JsonResponse(list(ingredient), safe=False)
        else:
            return redirect('/membre/')
    else:
        return redirect('/')

