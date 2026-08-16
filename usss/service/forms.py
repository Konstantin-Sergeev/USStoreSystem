from django import forms

class ProductForm(forms.Form):
    product_id = forms.CharField(required=False)
    product_code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    category = forms.CharField(required=False)
    is_coffee = forms.CharField(required=False)