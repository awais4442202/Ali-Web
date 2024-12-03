from django import forms
from .models import ContactMessage

from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']




class DeliveryForm(forms.Form):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Delivery Address",
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone Number",
        required=True
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label="Quantity",
        required=True
    )
