from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings

from compte.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from twilio.rest import Client
#
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.hashers import make_password
# from dotenv import load_dotenv
from .models import OTPVerification  # Nouveau modèle pour stocker les OTP temporairement
import random
from django.utils import timezone
from django.shortcuts import get_object_or_404
import phonenumbers
from django.urls import reverse

# Create your views here.def login_page(request):
##################
def signup_page(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur manuellement sans l'activer immédiatement
            username = form.cleaned_data['username']
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']

            user = User.objects.create(
                username=username,
                password=make_password(password),
                telephone=telephone,
                is_active=False  # L'utilisateur n'est pas encore actif
            )
            user.save()

            # Générer et envoyer un OTP
            otp = generate_otp()
            print("otp",otp)
            send_otp_sms(telephone, otp)

            # Enregistrer l'OTP dans un modèle temporaire avec une date d'expiration
            OTPVerification.objects.create(user=user, otp=otp, expiration_time=timezone.now() + timezone.timedelta(minutes=10))

            # Rediriger vers la page de vérification de l'OTP
            return redirect('compte:otp_verification', user_id=user.id)

    else:
        form = forms.SignupForm()
    return render(request, 'compte/signup.html', {'form': form})

##################
# def generate_otp():
#     return random.randint(100000, 999999)  # Génère un OTP à 6 chiffres

##################
def send_otp_sms(telephone, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message_body = f"Votre code de vérification est : {otp}"
    client.messages.create(
        to=telephone.as_e164,  # Numéro de téléphone au format E.164
        from_=settings.TWILIO_NUMBER,
        body=message_body
    )
#
def otp_verification(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        
        try:
            otp_verification = OTPVerification.objects.get(user=user, otp=otp_input)
            if otp_verification.is_valid():
                user.is_active = True
                user.save()
                
                otp_verification.delete()
                login(request, user)
                return redirect('pro_commerce:homepage')
            else:
                return render(request, 'compte/otp_verification.html', {'error': 'OTP invalide ou expiré.'})
        
        except OTPVerification.DoesNotExist:
            return render(request, 'compte/otp_verification.html', {'error': 'OTP incorrect.'})
    
    return render(request, 'compte/otp_verification.html', {'user': user})


##################
def login_page(request):
    id = None

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(telephone=telephone)

                if not user.is_active:
                    # Générer l'URL vers la page de saisie du code OTP
                    otp_verification_url = reverse('compte:otp_verification', kwargs={'user_id': user.id})
                    
                    # Ajouter une erreur avec un lien vers la page OTP
                    error_message = f'Votre compte n\'est pas encore activé. <a href="{otp_verification_url}">Cliquez ici pour entrer le code OTP</a>.'
                    form.add_error(None, error_message)
                else:
                    user = authenticate(username=user.username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('pro_commerce:homepage')
                    else:
                        form.add_error(None, 'Le numéro de téléphone ou le mot de passe est incorrect.')
            except User.DoesNotExist:
                form.add_error(None, 'Le numéro de téléphone ou le mot de passe est incorrect.')
    else:
        form = forms.LoginForm()

    return render(request, 'compte/login.html', {'form': form, 'id': id})

##################
def logout_user(request):
    logout(request)
    
    return redirect('pro_commerce:homepage')

#profile user
##################
@login_required
def profile(request):
    return render(request,'compte/profile_user.html')

##################
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('nouveau_mot_de_passe'):
                update_session_auth_hash(request, user)  # Met à jour la session pour éviter la déconnexion
            # messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('pro_commerce:homepage')
    else:
        form = forms.UserProfileForm(instance=user)
    
    return render(request, 'compte/profile_user.html', {'form': form})

##################
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('pro_commerce:homepage')  # Redirigez vers une page d'accueil ou de connexion après suppression
    return redirect('compte:profile')

##################
def password_reset_request(request):
    if request.method == 'POST':
        form = forms.PasswordResetRequestForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['telephone']
            print("non convert",phone_number)
            # Convertir l'objet PhoneNumber en chaîne E.164
            telephone_e164 = phone_number.as_e164
            print("convert",telephone_e164)
            try:
                # Vérifiez si l'utilisateur existe avec le numéro de téléphone donné
                user = User.objects.get(telephone=telephone_e164)
                
                # Générer un OTP et l'envoyer
                user.generate_otp()
                print("oooo",user.otp)
                broadcast_sms(telephone_e164, f"Votre code de réinitialisation est : {user.otp}")
                # Rediriger vers la page de vérification de l'OTP
                return redirect('compte:verify_otp', user_id=user.pk)
            except User.DoesNotExist:
                form.add_error(None, 'Aucun utilisateur trouvé avec ce numéro de téléphone.')

    else:
        form = forms.PasswordResetRequestForm()

    return render(request, 'compte/password_reset_request.html', {'form': form})

##################
import logging
logger = logging.getLogger(__name__)
def broadcast_sms(telephone, message_to_broadcast):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            to=telephone,
            from_=settings.TWILIO_NUMBER,
            body=message_to_broadcast
        )
        logger.info(f"Message SID: {message.sid}")
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")

##################
def verify_otp(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = forms.OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']

            # Vérifiez si l'OTP est correct et n'a pas expiré
            if user.otp == otp and timezone.now() < user.otp_expiry:
                return redirect('compte:password_reset_confirm', user_id=user.pk)  # Redirige vers la page de réinitialisation du mot de passe
            else:
                form.add_error(None, 'OTP incorrect ou expiré.')
    else:
        form = forms.OTPVerificationForm()

    return render(request, 'compte/verify_otp.html', {'form': form,'user':user})    

##################
def password_reset_confirm(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = forms.SetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password2']
            user.password = make_password(new_password)
            user.otp = None  # On supprime l'OTP après la réinitialisation
            user.otp_expiry = None
            user.save()

            return redirect('compte:password_reset_complete')
    else:
        form = forms.SetPasswordForm()

    return render(request, 'compte/password_reset_confirm.html', {'form': form,'user':user})

##################
def password_reset_complete(request):
    return render(request, 'compte/password_reset_complete.html')
