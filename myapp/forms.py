from django import forms
from .models import CalorieLog

class CalorieLogForm(forms.ModelForm):
    class Meta:
        model = CalorieLog
        fields = ['food_item', 'calories']
        widgets = {
            'food_item': forms.TextInput(attrs={
                'id': 'food_item',
                'placeholder': 'e.g., Rice and chicken...',
                'required': True
            }),
            'calories': forms.NumberInput(attrs={
                'id': 'calories',
                'placeholder': 'e.g., 450',
                'required': True
            }),
        }
