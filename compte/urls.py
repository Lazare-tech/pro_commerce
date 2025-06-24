from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
import compte.views
#

# path('',LoginView.as_view(template_name='compte/login.html',
#                           redirect_authenticated=True),
#      name='login'),
# path('logout/',LogoutView.as_view(),name='logout')
app_name= "compte"
urlpatterns = [
    path('login/',compte.views.login_page,name='login'),
    path('signup/',compte.views.signup_page,name='signup'),
    path('logout/',compte.views.logout_user,name='logout'),
    path('delete_account',compte.views.delete_account,name='delete_account'),
    path('profile',compte.views. profile_view,name='profile'),
        # path('profile_utilisateur/',compte.views.profile,name='profile'),
        path('sms_sent',compte.views.broadcast_sms,name='default'),
    path('password-reset/', compte.views.password_reset_request, name='password_reset_request'),
        path('otp_verification_user/<int:user_id>/', compte.views.otp_verification, name='otp_verification'),
        
  path('verify-otp/<int:user_id>/', compte.views.verify_otp, name='verify_otp'),
    path('password-reset-confirm/<int:user_id>/', compte.views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-complete/', compte.views.password_reset_complete, name='password_reset_complete'),
]
