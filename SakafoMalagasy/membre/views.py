from django.contrib.auth import logout
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "membre/index.html")
    else:
        return redirect('index')


def logouts(request):
    logout(request)
    return redirect('index')