from django.http import HttpResponse
from django.shortcuts import render


def Home(request):
    return HttpResponse('Home Page')


def Image(request):
    return HttpResponse('Image Page')
