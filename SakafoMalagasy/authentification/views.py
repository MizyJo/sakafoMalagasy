from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def register(request):
    return render(request, "authentification/register.html")


def vue_login(request):
    return render(request, 'authentification/login.html')


def tchek_login(request):
    if request.method == "POST":
        username = request.POST.get('pseudo')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/membre/')
        else:
            error_message = "Nom d'utilisateur ou mot dde passe incorrècte"
            return render(request, "authentification/login.html",{'error_message':error_message})
    else:
        redirect(reverse("/auth/login"))


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def email_existe_deja(email):
    # Vérifie si un utilisateur avec cet email existe déjà dans la base de données
    return User.objects.filter(email=email).exists()


def save_user(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpass = request.POST.get("confpass")
        username = request.POST.get("pseudo")

        if nom != "" and prenom != "" and email != "" and password != "" and confpass != "" and username != "":
            if is_valid_email(email) and len(nom) > 4 and len(prenom) > 4 and len(password) > 6 and len(username) > 4:
                if password == confpass:
                    if email_existe_deja(email):
                        error_message = "Votre email est déja enregistrer par un utilisateur"
                        return render(request, 'authentification/register.html', {'error_message': error_message})
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email, first_name=nom, last_name=prenom)
                        success_message = "Votre compte a été créer avec sucès"
                        return render(request,'authentification/register.html',{'success_message':success_message})
                else:
                    error_message = "Les deux champs de mot de passe doit etre identique"
                    return render(request, 'authentification/register.html', {'error_message': error_message})
            else:
                error_message = "Soit votre email n'est pas valide, soit les champs ne contient pas nombre minimum de contenu"
                return render(request, 'authentification/register.html', {'error_message': error_message})
        else:
            error_message = "Tous les champs sont obligatoire"
            return render(request, 'authentification/register.html', {'error_message': error_message})
    else:
        error_message = "Méthode non autaurisé"
        return render(request, 'authentification/register.html', {'error_message': error_message})



