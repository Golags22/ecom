from django.contrib import admin
from django.urls import path, include
from shop.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),  # For login/logout
    path('shop/', include('shop.urls')),
    path('', home, name='home'),
]
