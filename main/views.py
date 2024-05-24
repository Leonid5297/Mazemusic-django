from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def main_page(request):

    return render(request, "main/main_page.html")
