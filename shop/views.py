# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order, UserProfile, OrderItem  # Ensure all models are imported
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm  # Ensure you have this form defined
from django.views.generic import ListView

def home(request):
    # Fetch all products from sellers
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Create UserProfile
            login(request, user)
            return redirect('profile')  # Redirect to profile after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        is_seller = request.POST.get('is_seller') == 'on'
        user_profile = request.user.userprofile
        user_profile.is_seller = is_seller
        user_profile.save()
    return render(request, 'profile.html')  # Ensure this template exists

@login_required
def manage_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'manage_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the seller to the logged-in user
            product.save()
            return redirect('manage_products')  # Redirect to manage products
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1  # Increase quantity if item already in cart
        cart_item.save()
    return redirect('cart')  # Redirect to the cart view

@login_required
class CartView(ListView):
    model = CartItem
    template_name = 'shop/cart.html'  # Specify the correct template
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Filter based on the current user
        return CartItem.objects.filter(user=self.request.user)

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user, order__isnull=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total=total)
    cart_items.update(order=order)  # Associate cart items with the new order
    
    return render(request, 'shop/checkout.html', {'order': order})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  # Ensure the user is the seller
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')  # Redirect to manage products
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  # Ensure the user is the seller
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')  # Redirect to manage products
    return render(request, 'shop/delete_product.html', {'product': product})

def custom_logout(request):
    logout(request)
    return redirect('logout_success')  # Redirect to logout success page

@login_required
def order_confirmation(request):
    # Get the latest paid order for the logged-in user
    order = Order.objects.filter(user=request.user, is_paid=True).order_by('-created_at').first()
    
    if not order:
        return redirect('product_list')  # Redirect to the product list if no order found

    return render(request, 'store/order_confirmation.html', {'order': order})
