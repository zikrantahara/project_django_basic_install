from django.shortcuts import render

def index(request):
    return render(request, "index.html", {})

def register(request):
    return render(request, "base.html", {})

def login(request):
    return render(request, "base.html", {})

def handler404(request, exception):
    return render(request, '404handler.html')