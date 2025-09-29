from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from .forms import UserRegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)

        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать в наш магазин!',
            message=f'Приветствуем, {user.email}! Спасибо за регистрацию.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True