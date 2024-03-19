from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


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