from django.shortcuts import render
from .models import Product
# Create your views here.
def show_main(request):
    context = {
        'app_name' : 'Queen Kicks Store',
        'name': 'Maharani Anindya Budiarti',
        'class': 'KKI',

    }
    return render(request, "main.html", context)
