from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponseRedirect

def index(request):
    
    return HttpResponse("Hello, world. You're at the main index.")

