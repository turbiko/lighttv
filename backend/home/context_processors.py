from .forms import ContactForm  # Замініть на шлях до вашої форми

def contact_form(request):
    return {'form': ContactForm()}