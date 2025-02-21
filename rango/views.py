from django.shortcuts import render
from django.http import HttpResponse 

def index(request):
    return HttpResponse("Rango dice ¡Hola compañero! <a href='/rango/about/'> Ir a About</a>")

def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Volver al Inicio</a>")

