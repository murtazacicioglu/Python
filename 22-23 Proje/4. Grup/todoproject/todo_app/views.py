from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request): 
    return render(request,"todo_app/index.html")

def about(request):
    return render(request,"todo_app/about.html")
def kayit(request):
    return render(request,"todo_app/kayit.html")
def sifreunuttum(request):
        return render(request,"todo_app/sifreunuttum.html")
def giris1(request):
        return render(request,"todo_app/giris1.html")

