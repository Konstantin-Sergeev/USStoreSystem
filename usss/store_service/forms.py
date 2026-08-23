from django import forms

class StoreForm(forms.Form):
    store_id = forms.CharField(required=True)
    state = forms.CharField(required=False)
    market = forms.CharField(required=False)
    market_size = forms.CharField(required=False)
    store_code = forms.IntegerField(required=True)