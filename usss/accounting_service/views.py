from django.shortcuts import render, redirect
from service.models import Products
from store_service.models import Stores
from accounting_service.models import Accounting
from django.http import HttpResponse
from accounting_service.forms import FileForm, AccountingForm
import pandas as pd
import plotly.express as px
from django.db.models.functions import TruncMonth
from django.db.models import Sum
import plotly.graph_objects as go

def get_chart():
    # Агрегация по месяцам со всеми показателями
    data = (
        Accounting.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            total_sales=Sum('sales'),
            total_cogs=Sum('COGS'),
            total_marketing=Sum('marketing_expenses'),
            total_other=Sum('other_expenses')
        )
        .order_by('month')
    )
    
    df = pd.DataFrame(list(data))
    df['month_str'] = df['month'].dt.strftime('%B %Y')
    
    # Считаем маржу
    df['margin'] = df['total_sales'] - df['total_cogs'] - df['total_marketing'] - df['total_other']
    df['margin_percent'] = (df['margin'] / df['total_sales'] * 100).round(2)
    
    # Создаем график с двумя осями
    fig = go.Figure()
    
    # 1. Колонки - продажи (основная ось)
    fig.add_trace(go.Bar(
        x=df['month_str'],
        y=df['total_sales'],
        name='Продажи',
        marker_color='#ff9000',
        marker_line_color='#cc7200',
        marker_line_width=1,
        yaxis='y',
        opacity=0.8
    ))
    
    # 2. Линия - маржа (вторая ось)
    fig.add_trace(go.Scatter(
        x=df['month_str'],
        y=df['margin'],
        name='margin',
        mode='lines+markers',
        line=dict(color='#00ff88', width=3),
        marker=dict(color='#00ff88', size=10, symbol='diamond'),
        yaxis='y2'
    ))
    
    # 3. Текст с процентами на точках маржи
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['month_str'],
            y=row['margin'],
            text=f"{row['margin_percent']}%",
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor='#00ff88',
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.6)',
            bordercolor='#00ff88',
            borderwidth=1,
            borderpad=4,
            yshift=10
        )
    
    # Настройка layout с двумя осями
    fig.update_layout(
        title=dict(
            text='Sales & margin by months',
            font=dict(color='white', size=24)
        ),
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font_color='#e0e0e0',
        
        # Основная ось (продажи)
        yaxis=dict(
            title=dict(text='Sales', font=dict(color='#FFFFFF')),
            tickfont=dict(color='#e0e0e0'),
            gridcolor='#333333',
            zerolinecolor='#444444',
            side='left'
        ),
        
        # Вторая ось (маржа)
        yaxis2=dict(
            title=dict(text='Маржа', font=dict(color='#00ff88')),
            tickfont=dict(color='#e0e0e0'),
            gridcolor='#333333',
            zerolinecolor='#444444',
            overlaying='y',
            side='right'
        ),
        
        # Ось X
        xaxis=dict(
            tickangle=45,
            gridcolor='#333333',
            tickfont=dict(color='#e0e0e0')
        ),
        
        # Легенда
        legend=dict(
            font=dict(color='#e0e0e0'),
            bgcolor='rgba(31,31,31,0.8)',
            bordercolor='#444444',
            borderwidth=1
        ),
        
        # Отступы
        margin=dict(l=60, r=60, t=80, b=80),
        
        # Ховер-режим
        hovermode='x unified'
    )

    return fig.to_html(full_html=False)

def accounting_service_page(request):
    existing_products = Products.objects.all()
    existing_stores = Stores.objects.all()
    chart_html = get_chart()
    return render(request, template_name='accounting_service/accounting_service.html', context= {'existing_products': existing_products,
                                                                                                 'existing_stores' : existing_stores,
                                                                                                 'chart_html': chart_html})

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

            











