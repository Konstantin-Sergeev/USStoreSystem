from django.shortcuts import render, redirect
from service.models import Stores, Products
from accounting_service.models import Accounting
from django.http import HttpResponse
from accounting_service.forms import FileForm
import pandas as pd

def accounting_service_page(request):
    return render(request, template_name='accounting_service/accounting_service.html')

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









