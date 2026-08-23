from django.urls import path, include
from store_service import views

urlpatterns = [
    path('', views.stores_page, name='stores_page'),
    path('save/', views.stores_page_save, name='stores_page_save')
]