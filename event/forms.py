from django import forms
from .models import Event ,Category # Make sure you have an Event model in models.py

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500'}),
        }