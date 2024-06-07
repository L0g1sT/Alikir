from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, PasswordResetForm
from users.models import User, EmailVerification
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Алькир - авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Алькир - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Алькир - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Алькир - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()

            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index')) 




class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetSendView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = get_user_model().objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Отправка сообщения электронной почты с инструкциями по восстановлению пароля
        subject = 'Восстановление пароля'
        message = f'Здравствуйте, {user.get_full_name()}.\n\nВы запросили восстановление пароля для вашей учетной записи.\n\nДля восстановления пароля перейдите по следующей ссылке: http://alikirrostov.ru/users/password_reset_confirm/{uidb64}/{token}/\n\nЕсли вы не запрашивали восстановление пароля, просто проигнорируйте это письмо.\n\nС уважением,\nАдминистрация сайта.'
        send_mail(
            subject=subject,
            message=message,
            from_email='lfdblxa123@yandex.ru',
            recipient_list=[email],
        )

        messages.success(self.request, 'Сообщение с инструкциями по восстановлению пароля отправлено на ваш адрес электронной почты.')
        return redirect('users:login')


class UserPasswordResetConfirmView(TitleMixin, PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    title = 'Алькир - Подтверждение сброса пароля'


class UserPasswordResetCompleteView(TitleMixin, PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    title = 'Алькир - Пароль успешно сброшен'