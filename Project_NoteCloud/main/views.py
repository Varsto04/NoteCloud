from django.shortcuts import render, redirect


def index(request):
    return render(request, 'main/index.html')


def developers(request):
    return render(request, 'main/developers.html')


def installation(request):
    return render(request, 'main/installation.html')


def login(request):
    return redirect('authorization:login')
