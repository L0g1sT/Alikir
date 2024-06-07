from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Иванов'}))
    email = forms.EmailInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'you@email.com'})
    address = forms.CharField(widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))
    basket_history = forms.JSONField()

            
    class Meta:
        model = Order
        fields = (
                'first_name', 'last_name',
                'email', 'address', 'basket_history')
