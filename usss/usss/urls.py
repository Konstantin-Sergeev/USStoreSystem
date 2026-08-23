from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('service.urls')),
    path('accounting/', include('accounting_service.urls')),
    path('stores/', include('store_service.urls')),
]
