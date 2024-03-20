from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from membre.models import Recette


# Create your views here.
def index(request):
    return render(request, "administrateur/login_admin.html")


def login_admin(request):
    if request.method == "POST":
        username = request.POST.get('pseudo')
        password = request.POST.get('password')

        if username != "" and password != "":
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/administrateur/dashboard')
            else:
                return render(request, "administrateur/login_admin.html", {"error_message": "Nom d'utilisateur ou mot de passe incorrecte ou vous n'êtes pas un admin"})
        else:
            return render(request, "administrateur/login_admin.html",
                          {"error_message": "Tous les champ sont obligatoire"})
    else:
        return redirect('/administrtateur')


def dashboard(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        return render(request, "administrateur/index.html", {'users': users, 'active_page': 'users'})
    else:
        return redirect('/administrateur')


def desactive_user(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=id)
        if user.is_active:
            user.is_active = False
            user.save()
        elif not user.is_active:
            user.is_active = True
            user.save()
        print(user.is_active)
        return redirect('/administrateur/dashboard')

    else:
        return redirect('/administrateur')


def delete_user(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('/administrateur/dashboard')
    else:
        return redirect('/administrateur')


def liste_recette(request):
    if request.user.is_authenticated:
        recette = Recette.objects.all()
        return render(request, 'administrateur/liste_recette.html', {'active_page': 'liste_recette', 'recette': recette})
    else:
        return redirect('/')


def last_login(request):
    if request.user.is_authenticated:
        derniers_utilisateurs = User.objects.filter(last_login__gte=datetime.now() - timedelta(days=1))
        return render(request, "administrateur/last_login.html", {'user': derniers_utilisateurs, 'active_page': 'last_login'})
    else:
        return redirect('/administrateur')

