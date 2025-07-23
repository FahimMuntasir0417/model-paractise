from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk
    activation_link = request.build_absolute_uri(
        reverse('activate', args=[uid, token])
    )
    subject = 'Activate your account'
    message = f'Hi {user.username},\n\nPlease activate your account:\n{activation_link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)