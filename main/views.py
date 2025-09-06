from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app_name' : 'Queen Kicks',
        'name': 'Maharani Anindya Budiarti',
        'class': 'KKI'
    }

    return render(request, "main.html", context)