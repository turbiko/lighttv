from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from email.header import Header
from django.core.mail import get_connection

from .forms import ContactForm


def submit_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Form valid, send some data')
            subject = "site form"
            message = f"From: {form.cleaned_data['name']}<br>Email: {form.cleaned_data['email']}<br>Message: {form.cleaned_data['message']}"
            admin_emails = [email for name, email in settings.ADMINS]

            if settings.DEBUG:
                send_mail(
                    subject,
                    message,
                    settings.SERVER_EMAIL,
                    admin_emails,
                    fail_silently=False,
                    html_message=message,
                )
            else:
                # block send and debug session smtp
                connection = get_connection()
                connection.open()
                connection.connection.set_debuglevel(1)
                # block send and debug session: send email with debug
                send_mail(
                    subject,
                    message,
                    settings.SERVER_EMAIL,
                    admin_emails,
                    fail_silently=False,
                    html_message=message,
                    connection=connection,
                )
                connection.close()
                # block send and debug session: close connection

            # Додайте повідомлення або здійсніть перенаправлення
            messages.success(request, 'Ваше повідомлення успішно надіслано!')
            print(f'{message=}')
            return redirect('/')
        else:
            print('Form NOT valid, can`t send data')
            messages.error(request, 'Виникла помилка при надсиланні повідомлення.')
    else:
        print('Form new')
        form = ContactForm()
    # Якщо щось пішло не так, перенаправте користувача назад на форму
    return redirect('/')
