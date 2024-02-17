from django.shortcuts import render, HttpResponse


def index(request, *args, **kwargs):
    return HttpResponse('Hello, world!')
