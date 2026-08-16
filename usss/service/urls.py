from django.urls import path, include
from service import views

urlpatterns = [
    path('', views.products_page, name='products_page'),
    path('save/', views.products_page_save, name='products_page_save')
]
