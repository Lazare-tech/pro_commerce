from django import forms
from pro_commerce.models import *
from rating.models import ReviewRating
from phonenumber_field.formfields import PhoneNumberField

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = ReviewRating
#         fields = ['subject', 'review', 'rating']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5}),
        }