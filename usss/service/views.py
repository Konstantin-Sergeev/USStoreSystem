from django.shortcuts import render, redirect
from service.models import Stores, Products
from django.http import HttpResponse
from service.forms import ProductForm

def products_page(request):
    products = Products.objects.all()
    return render(request, template_name='service/products_page.html', context={'products': products})

def products_page_save(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.data
            object = Products.objects.get(id = data.get('product_id'))
            object.product_code = data.get('product_code')
            object.name = data.get('name')
            object.category = data.get('category')
            object.is_coffee = data.get('is_coffee')
            object.save()
        else:
            print(form.errors)

    return redirect(products_page)