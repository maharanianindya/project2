from django.urls import path
from main.views import show_main, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import add_product, product_detail
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import edit_product
from main.views import delete_product
from main.views import add_product_entry_ajax
from main.views import update_product_ajax
from main.views import login_ajax, register_ajax, logout_ajax, proxy_image,create_product_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),
    path('product/<str:id>/', product_detail, name='product_detail'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:prod_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:prod_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<int:id>/edit', edit_product, name='edit_product'),
    path('product/<int:id>/delete', delete_product, name='delete_product'),
    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('product/update-ajax/', update_product_ajax, name='update_product_ajax'),
    path("login-ajax/", login_ajax, name="login_ajax"),
    path("register-ajax/", register_ajax, name="register_ajax"),
    path("logout-ajax/", logout_ajax, name="logout_ajax"),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),


    
]
