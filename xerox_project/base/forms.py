# xerox_app/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','price']

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
    
class CustomerForm(forms.Form):
    name = forms.CharField(max_length=255, label='Your Name')