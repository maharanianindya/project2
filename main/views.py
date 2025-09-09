from django.shortcuts import render
from .models import Product
# Create your views here.
def show_main(request):
    products = Product.objects.all()
    context = {
        'app_name' : 'Queen Kicks Store',
        'name': 'Maharani Anindya Budiarti',
        'class': 'KKI',
        'products': products,
    }
    return render(request, "main.html", context)
