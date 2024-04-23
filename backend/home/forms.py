from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше ім’я', max_length=230,
                           widget=forms.Textarea(attrs={'placeholder': 'Ваше ім\'я', 'cols': '15', 'rows': '1'}), )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ваша пошта',
            'maxlength': '235',  # Максимальна кількість символів
        }))
    message = forms.CharField(label='Ваше питання...',
                              widget=forms.Textarea(attrs={
                                  'placeholder': 'Ваше питання...', 'cols': '35', 'rows': '1'}), )
