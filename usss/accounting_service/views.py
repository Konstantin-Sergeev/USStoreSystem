from django.shortcuts import render, redirect
from service.models import Products
from store_service.models import Stores
from accounting_service.models import Accounting
from django.http import HttpResponse
from accounting_service.forms import FileForm, AccountingForm
import pandas as pd

def accounting_service_page(request):
    existing_products = Products.objects.all()
    existing_stores = Stores.objects.all()
    return render(request, template_name='accounting_service/accounting_service.html', context= {'existing_products': existing_products,
                                                                                                 'existing_stores' : existing_stores})

def to_float(text) -> float:
    if text and pd.notna(text):
        return float(text)
    return 0

def to_date(date):
    year = '20' + date[date.find(' ') - 2: date.find(' ')]
    month = date[date.find('/') + 1: date.find('/') + 3]
    day = date[date.find('/') - 2: date.find('/')]
    data = year + '-' + month + '-' + day
    return data

def find_product(product_code, name):
    productObjects = Products.objects.filter(product_code = product_code)
    if len(productObjects) > 0:
        return productObjects[0]
    object = Products(product_code = product_code, name = name, is_coffee = 0)
    object.save()
    return object
        
def process_file(file):
    df =  pd.read_csv(file)
    for _, row in df.iterrows():
        product_code = row.get('ProductId')
        name = row.get('product')
        productObject = find_product(product_code, name)
        store_code = row.get('Area Code')
        state = row.get('State')
        storeObject, _ = Stores.objects.get_or_create(store_code = store_code, state = state)
        date = to_date(row.get('Date'))
        sales = to_float(row.get('Sales'))
        COGS = to_float(row.get('COGS'))
        marketing_expenses = to_float(row.get('Marketing expenses'))
        other_expenses = to_float(row.get('Total Expenses')) - marketing_expenses
        accountingObject = Accounting.objects.get_or_create(date = date, product = productObject, store = storeObject)[0]
        accountingObject.sales = sales
        accountingObject.COGS = COGS
        accountingObject.marketing_expenses = marketing_expenses
        accountingObject.other_expenses = other_expenses
        accountingObject.save()

def accounting_file_save(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get('file')
            process_file(file)
        else:
            print(form.errors)
    return redirect(accounting_service_page)

def accounting_row_save(request):
    if request.method == 'POST':
        form = AccountingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            accounting_object = Accounting()
            accounting_object.date = data.get('date')
            accounting_object.product = Products.objects.get(id = data.get('product'))
            accounting_object.store = Stores.objects.get(id = data.get('store'))
            accounting_object.sales = to_float(data.get('sales')) * (-1 if data.get('return_flag') else 1)
            accounting_object.COGS = to_float(data.get('COGS')) * (-1 if data.get('return_flag') else 1)
            accounting_object.marketing_expenses = to_float(data.get('marketing_expenses')) * (-1 if data.get('return_flag') else 1)
            accounting_object.other_expenses = to_float(data.get('other_expenses')) * (-1 if data.get('return_flag') else 1)
            accounting_object.save()
        else:
            print(form.errors)
    return redirect(accounting_service_page)

            











