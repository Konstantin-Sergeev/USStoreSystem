from django.shortcuts import render, redirect
from store_service.models import Stores
from django.http import HttpResponse
from store_service.forms import StoreForm

def stores_page(request):
    stores = Stores.objects.all()
    return render(request, template_name = 'store_service/stores_page.html', context = {'stores':stores})

def stores_page_save(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            store_object = Stores.objects.get(id = data.get('store_id'))
            store_object.state = data.get('state')
            store_object.market = data.get('market')
            store_object.market_size = data.get('market_size')
            store_object.store_code = data.get('store_code')
            store_object.save()
        else:
            print(form.errors)
    return redirect(stores_page)