from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.signals import user_logged_out, user_logged_in, user_login_failed
from django.contrib import messages


@receiver(post_save, sender=Booking)
def send_booking_mail(sender, instance, created, **kwargs):
    print("Instance", instance.user.email)
    if created:
        user_email = instance.user.email
        costume_name = instance.costume.name
        start = instance.start_date
        end = instance.end_date

        subject = 'Costume Booking Confirmation'
        message = f'Hi {user_email},\n\nYour booking for "{costume_name}" from {start} to {end} has been confirmed. Thank you!'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )


@receiver(user_logged_out)
def show_logged_out_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out successfully.')


@receiver(user_logged_in)
def show_logged_in_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged in successfully.')


@receiver(user_login_failed)
def show_login_failed_message(sender, request, credentials, **kwargs):
    messages.error(request, 'Login failed. Please try again.')