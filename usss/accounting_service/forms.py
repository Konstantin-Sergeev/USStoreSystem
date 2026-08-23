from django import forms

class FileForm(forms.Form):
    file = forms.FileField(required=True)

class AccountingForm(forms.Form):
    date = forms.DateField(required=True)
    product = forms.IntegerField(required=True)
    store = forms.IntegerField(required=True)
    sales = forms.FloatField(required=True)
    COGS = forms.FloatField(required=True)
    marketing_expenses = forms.FloatField(required=True)
    other_expenses = forms.FloatField(required=True)
    return_flag = forms.BooleanField(required=False)
