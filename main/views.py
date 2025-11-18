from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from main.forms import ProductForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    cat = request.GET.get("category", "")

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
    if cat: 
        product_list = product_list.filter(category=cat)

    context = {
        'app_name' : 'Queen Kicks Store',
        'name': request.user.username,
        'class': 'KKI',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'), 
        'NAV_CATEGORIES': [                               # ← added
            {'value': v, 'label': l} for v, l in Product.CATEGORY_CHOICES
        ],
        'ACTIVE_CATEGORY': cat,
    }
    return render(request, "main.html", context)

def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect ('main:show_main')
    context = {
        'form': form
    }
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        'product': product
    }
    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    product_list = Product.objects.all()
    cat = request.GET.get("category", "").strip()
    if cat:
        product_list = product_list.filter(category=cat)

    data = [{
        'id': str(product.id),
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'thumbnail': product.thumbnail,
        'is_featured': product.is_featured,
        'user_id': product.user_id or 0,
    } for product in product_list]
    return JsonResponse(data, safe=False)


def show_xml_by_id(request, prod_id):
    try:
        prod_item = Product.objects.filter(pk=prod_id)
        xml_data = serializers.serialize("xml", prod_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
def show_json_by_id(request, prod_id):
    try:
        product = Product.objects.select_related('user').get(pk=prod_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'price': product.price,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {
    'form': form
    }
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name")) # strip HTML tags!
    description = strip_tags(request.POST.get("description")) # strip HTML tags!
    category = request.POST.get("category")
    price = request.POST.get("price")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_product = Product(
        name=name, 
        description=description,
        category=category,
        price = price,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()
    return HttpResponse(b"CREATED", status=201)

@login_required
@require_POST
def update_product_ajax(request):
    prod_id = (request.POST.get('id') or '').strip()
    if not prod_id:
        return JsonResponse({"ok": False, "msg": "Missing product id."}, status=400)

    product = get_object_or_404(Product, pk=prod_id, user=request.user)

    name        = (request.POST.get('name') or '').strip()
    description = (request.POST.get('description') or '').strip()
    category    = (request.POST.get('category') or '').strip()
    price       = (request.POST.get('price') or '').strip()
    thumbnail   = (request.POST.get('thumbnail') or '').strip()
    is_featured = request.POST.get('is_featured') in ['on', 'true', '1']

    if not name or not description or not category or price == '':
        return JsonResponse({"ok": False, "msg": "Missing required fields."}, status=400)

    try:
        product.name        = name
        product.description = description
        product.category    = category 
        product.price       = int(price)  
        product.thumbnail   = thumbnail
        product.is_featured = is_featured
        product.save()
    except Exception as e:
        return JsonResponse({"ok": False, "msg": str(e)}, status=400)

    return JsonResponse({"ok": True})

@require_POST
def login_ajax(request):
    u = request.POST.get('username','').strip()
    p = request.POST.get('password','')
    user = authenticate(request, username=u, password=p)
    if user:
        login(request, user)
        response = JsonResponse({
            "ok": True, 
            "username": user.username,
            "message": f"Welcome back, {user.username}!"
        })
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    return JsonResponse({"ok": False, "message": "Invalid username or password."}, status=400)

@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        first_err = next(iter(form.errors.values()))[0]
        return JsonResponse({"ok": False, "message": first_err}, status=400)
    user = form.save()
    login(request, user)
    # Set cookie for last_login
    response = JsonResponse({
        "ok": True, 
        "username": user.username,
        "message": f"Welcome, {user.username}! Your account has been created."
    })
    response.set_cookie('last_login', str(datetime.datetime.now()))
    return response
@require_POST
def logout_ajax(request):
    logout(request)
    messages.info(request, "You’ve been logged out. See you soon! 👋")
    return JsonResponse({"ok": True, "redirect": reverse("main:login")})

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        price = data.get("price", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_product = Product(
            name=name, 
            description=description,
            price = price,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)










    
