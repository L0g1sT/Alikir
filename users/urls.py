from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from users.views import UserLoginView, UserRegistrationView, UserProfileView, EmailVerificationView, \
    UserPasswordResetView, PasswordResetSendView, UserPasswordResetConfirmView, UserPasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_send/', PasswordResetSendView.as_view(), name='password_reset_send'),
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
