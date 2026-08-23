from django import forms

class StoreForm(forms.Form):
    store_id = forms.CharField(required=False)
    state = forms.CharField(required=True)
    market = forms.CharField(required=True)
    market_size = forms.CharField(required=True)
    store_code = forms.IntegerField(required=True)