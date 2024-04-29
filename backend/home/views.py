from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from email.header import Header
from django.core.mail import get_connection

from .forms import ContactForm
from .models import Contact


def submit_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Form valid, send some data')
            subject = "site form"
            message = f"From: {form.cleaned_data['name']}<br>Email: {form.cleaned_data['email']}<br>Message: {form.cleaned_data['message']}"
            admin_emails = [email for name, email in settings.ADMINS]
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )


            # Додайте повідомлення або здійсніть перенаправлення
            messages.success(request, 'Ваше повідомлення успішно збережено!')
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
