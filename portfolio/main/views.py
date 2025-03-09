from django.shortcuts import render, redirect
from .models import Artwork
from .forms import Commission, Contact
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return render(request, 'home.html', {
        'name': 'Sophie Hina Sato',
        'bio': 'bio',
        'art': Artwork.objects.all()
    })

def commission(request):
    domain_url = f"{request.scheme}://{request.get_host()}/"
    return render(request, 'commission.html', {'form': Commission()})

def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = f"{request.scheme}://{request.get_host()}"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1R0c6nEmJx4F4RCUrpD75c55',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain_url + '/checkout-landing/success/',
            cancel_url=domain_url + '/checkout-landing/cancelled/',
        )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
def checkout_landing(request, status):
    return render(request, 'checkout.html', {'status': status})

def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            email, message = form.cleaned_data['email'], form.cleaned_data['message']
            send_mail(f'Contact Form Submission from {email}', message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('home')
    else:
        form = Contact()
    return render(request, 'contact.html', {'form': Contact()})