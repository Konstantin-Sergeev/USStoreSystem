from django.urls import path, include
from accounting_service import views

urlpatterns = [
    path('', views.accounting_service_page, name='accounting_service_page'),
    path('save-file/', views.accounting_file_save, name='accounting_file_save'),
    path('save/', views.accounting_row_save, name = 'accounting_row_save'),
]