from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from membre.models import Recette, Photo, Etape, Ingredient, Favoris, Recette_a_faire, Recette_effectue


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
    return redirect('/')


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
            etape = Etape.objects.filter(recette_id=recette_id).values('numero', 'description')
            recette = Recette.objects.get(pk=recette_id)
            r = {
                'nom': recette.titre,
                'description': recette.description,
                'etape': list(etape)
            }
            return JsonResponse(list(etape), safe=False)
        else:
            return redirect('/membre/')
    else:
        return redirect('/')


def get_ingredient(request, recette_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            ingredient = Ingredient.objects.filter(recette_id=recette_id).values('nom')
            recette = get_object_or_404(Recette, id=recette_id)
            data = {
                'nom': recette.titre,
                'description': recette.description,
                'ingredient': list(ingredient)
            }
            return JsonResponse(list(ingredient), safe=False)
        else:
            return redirect('/membre/')
    else:
        return redirect('/')


def get_recette(request, recette_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            recette = Recette.objects.get(pk=recette_id)
            ingredients = list(Ingredient.objects.filter(recette_id=recette_id).values('id', 'nom'))
            etapes = list(Etape.objects.filter(recette_id=recette_id).values('id', 'numero', 'description'))

            data = {
                'id': recette.id,
                'titre': recette.titre,
                'description': recette.description,
                'etapes': etapes,
                'ingredients': ingredients
            }
            return JsonResponse(data)
        return redirect('/membre/recette')
    return redirect('/')


def add_etape(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id_recette = request.POST.get('id_recette')
            recette = get_object_or_404(Recette, pk=id_recette)
            numero = request.POST.get('numero')
            description = request.POST.get('description')
            if numero != "" and description != "":
                etape = Etape.objects.create(numero=numero, description=description, recette=recette)
                etape.save()
                return JsonResponse({'success': True})
            else:
                # Si la méthode de la requête n'est pas POST, renvoyer une erreur
                return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        else:
            return redirect('/membre/recette')
    else:
        return redirect('/membre')


def add_ingredient(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id_recette = request.POST.get('id_recette')
            recette = get_object_or_404(Recette, pk=id_recette)
            nom = request.POST.get('nom')
            if nom != "":
                ingredient = Ingredient.objects.create(nom=nom, recette=recette)
                ingredient.save()
                return JsonResponse({'success': True})
            else:
                # Si la méthode de la requête n'est pas POST, renvoyer une erreur
                return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        else:
            return redirect('/membre/recette')
    else:
        return redirect('/membre')


def add_favoris(request, recette_id=None):
    active_page = "add_favoris"
    if request.user.is_authenticated:
        if request.method == 'POST' and recette_id is not None:
            recette = get_object_or_404(Recette, pk=recette_id)
            favoris, created = Favoris.objects.get_or_create(utilisateur=request.user)
            favoris.recette.add(recette)
            return redirect(reverse('add_favoris_all'))
        else:
            favoris = Favoris.objects.filter(utilisateur=request.user)
            favoris_utilisateur = Favoris.objects.filter(utilisateur=request.user)
            return render(request, 'membre/add_favoris.html', {'active_page': active_page, 'favoris': favoris, 'favoris_utilisateur': favoris_utilisateur})
    else:
        return redirect('/')



def remove_favoris(request, recette_id):
    if request.method == 'POST':
        favoris = get_object_or_404(Favoris, utilisateur=request.user)
        favoris.recette.remove(recette_id)
        return redirect('add_favoris_all')  # Rediriger vers la page des favoris après la suppression



def get_etape_by_id(request, etape_id):
    etape = Etape.objects.get(pk=etape_id)
    if etape is not None:
        data = {
            'id': etape.id,
            'numero': etape.numero,
            'description': etape.description
        }
        return JsonResponse(data)
    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une erreur
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def get_ingredient_by_id(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    if ingredient is not None:
        data = {
            'id': ingredient.id,
            'nom': ingredient.nom
        }
        return JsonResponse(data)
    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une erreur
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def edit_etape(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST.get('id_etape')
            numero = request.POST.get('numero')
            description = request.POST.get('description')
            if id != "" and numero != "" and description != "":
                etape = Etape.objects.get(pk=id)
                if etape is not None:
                    etape.numero = numero
                    etape.description = description
                    etape.save()
                    return JsonResponse({'Success': True})
                else:
                    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
            else:
                return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        else:
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    else:
        return redirect('/')


def edit_ingredient(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST.get('id_ingredient')
            nom = request.POST.get('nom')
            if id != "" and nom != "":
                etape = Ingredient.objects.get(pk=id)
                if etape is not None:
                    etape.nom = nom
                    etape.save()
                    return JsonResponse({'Success': True})
                else:
                    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
            else:
                return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        else:
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    else:
        return redirect('/')



def delete_recette(request):
    if request.method == "POST":
        id = request.POST.get('id_recette')
        recette = get_object_or_404(Recette, pk=id)
        recette.delete()
        return JsonResponse({'Success': True})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def delete_etape(request):
    if request.method == "POST":
        id = request.POST.get('id_etape')
        etape = get_object_or_404(Etape,pk=id)
        etape.delete()
        return JsonResponse({'Success': True})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def delete_ingredient(request):
    if request.method == "POST":
        id = request.POST.get('id_ingredient')
        ingredient = get_object_or_404(Ingredient, pk=id)
        ingredient.delete()
        return JsonResponse({'Success': True})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def edit_recette(request):
    if request.method == "POST":
        id = request.POST.get('id_recette')
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        recette = get_object_or_404(Recette, pk=id)
        recette.titre = titre
        recette.description = description
        recette.save()
        return JsonResponse({'Success': True})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def affiche_recette(request, recette_id):
    if request.method == "GET":
        recette = get_object_or_404(Recette, pk=recette_id)
        photo = recette.photo.fichier.url
        profil = recette.auteur.profile.image.url
        data = {
            'id': recette.id,
            'titre': recette.titre,
            'description': recette.description,
            'photo': photo,
            'profil': profil,
            'date': recette.date_creation
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def recette_a_faire(request, recette_id):
    recette = Recette.objects.get(pk=recette_id)
    if Recette_a_faire.objects.filter(recette_id=recette_id, user_id=request.user.id).exists() or Recette_effectue.objects.filter(recette_id=recette_id, user_id=request.user.id).exists():
       return render(request, "membre/index.html", {'recette': Recette.objects.all(), 'active_page': 'explorer', 'error_message': "Cette recette est déja dans votre recette à faire ou dans votre recette appliqué"})
    else:
        Recette_a_faire.objects.create(recette=recette, user=request.user)
        recette_a_faire = Recette_a_faire.objects.filter(user=request.user)
        return render(request, 'membre/recette_a_faire.html',
                      {'active_page': 'recette_a_faire', 'recette': recette_a_faire, 'success_message': "recette ajouté avec succès"})


def liste_raf(request):
    recette = Recette_a_faire.objects.filter(user_id=request.user.id)
    return render(request, "membre/recette_a_faire.html", {'recette': recette, 'active_page': 'recette_a_faire'})


def recette_effectue(request, recette_id):
    if request.user.is_authenticated:
      raf = Recette_a_faire.objects.filter(recette_id=recette_id)
      recette = Recette.objects.get(pk=recette_id)
      user = request.user
      Recette_effectue.objects.create(recette=recette, user=user)
      raf.delete()
      recette_effectue = Recette_effectue.objects.filter(user=request.user)
      return render(request, "membre/recette_effectue.html", {'active_page': "recette_effectue", 'recette': recette_effectue, 'success_message': "Recette appliqué :)"})
    else:
        return redirect('/')


def liste_re(request):
    if request.user.is_authenticated:
        re = Recette_effectue.objects.filter(user=request.user)
        return render(request, "membre/recette_effectue.html", {'active_page': 'recette_effectue', 'recette': re})
    else:
        return redirect('/')