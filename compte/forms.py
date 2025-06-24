# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from compte.models import User
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    #change number to username if need username and password to connect
    telephone = forms.CharField(max_length=63, label='Numero de telephone')

    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
#

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label=_('Nom d’utilisateur'),
        error_messages={
            'required': _('Le nom d’utilisateur est requis.'),
            'max_length': _('Le nom d’utilisateur ne peut pas dépasser 63 caractères.')
        }
    )

    telephone = PhoneNumberField(
        label=_('Numéro de téléphone'),
        widget=forms.TextInput(attrs={
            'class': 'form-control intl-tel-input',  # Ajout de la classe pour intl-tel-input
            'placeholder': 'Entrez votre numéro de téléphone'
        }),
        error_messages={
            'required': _('Le numéro de téléphone est requis.'),
            'invalid': _('Entrez un numéro de téléphone valide.')
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Mot de passe'),
        min_length=6,
        error_messages={
            'required': _('Le mot de passe est requis.'),
            'min_length': _('Le mot de passe doit contenir au moins 6 caractères.')
        }
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Confirmer le mot de passe'),
        error_messages={
            'required': _('La confirmation du mot de passe est requise.')
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Les mots de passe ne correspondent pas.'))
    #
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Les mots de passe ne correspondent pas.'))

#
class UserProfileForm(forms.ModelForm):
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label="Nouveau mot de passe",
        required=False
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmer le mot de passe",
        required=False
    )
    
    
    class Meta:
        model = User
        fields = ['username', 'photo','telephone']
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # 'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'confirmer_mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),



            
        }
    def clean(self):
            cleaned_data = super().clean()
            new_password = cleaned_data.get('nouveau_mot_de_passe')
            confirm_password = cleaned_data.get('confirmer_mot_de_passe')

            if new_password and new_password != confirm_password:
                self.add_error('confirmer_mot_de_passe', "Les mots de passe ne correspondent pas.")

            return cleaned_data


class PasswordResetRequestForm(forms.Form):
    telephone = PhoneNumberField(
        label='Numéro de téléphone',
        error_messages={
            'invalid': 'Entrez un numéro de téléphone valide.',
            'required': 'Le numéro de téléphone est requis.'
        }
    )
#
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Entrez le code OTP")
#
# class SetPasswordForm(forms.Form):
#     new_password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("new_password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError("Les mots de passe ne correspondent pas.")
#         return cleaned_data

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nouveau Mot de Passe',
        widget=forms.PasswordInput,
        help_text="Le mot de passe doit contenir au moins 8 caractères."
    )
    new_password2 = forms.CharField(
        label='Confirmez le Mot de Passe',
        widget=forms.PasswordInput,
        help_text="Entrez à nouveau le mot de passe pour confirmation."
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
