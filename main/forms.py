from django.forms import ModelForm
from main.models import Product
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]

    category = forms.ChoiceField(choices=[ ('jersey', 'Jersey'),('footwear', 'Footwear'),('apparel', 'Apparel'),('accessories', 'Accessories'),])

