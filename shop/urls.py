from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register, user_login, profile, manage_products, 
    add_product, edit_product, delete_product, 
    product_detail, add_to_cart, checkout, 
    order_confirmation, custom_logout, CartView
)
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout-success/', TemplateView.as_view(template_name='registration/logout_success.html'), name='logout_success'),
    path('logout/', custom_logout, name='logout'),
    path('cart/', CartView, name='cart'),  
    path('profile/', profile, name='profile'),  
    path('manage-products/', manage_products, name='manage_products'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
