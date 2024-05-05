import stripe
import requests
import random
import string
import io
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket
stripe.api_key = settings.STRIPE_SECRET_KEY


CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
SHORTCODE = 'your_shortcode'
PASSKEY = 'your_passkey'
INITIATE_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

def home(request):
    print(request.user)
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        if not (username and email and password and confirm_password):
            errors.append('All fields are required.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        if User.objects.filter(email=email).exists():
            errors.append('Email is already registered.')

        if errors:
            return JsonResponse({'errors': errors}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('signin')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
            return redirect(request, 'home')
        else:
            return JsonResponse('error')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('home')  

def events(request):
    print(request.user)
    return render(request, 'events.html', {'events': events})

def buy_events(request):
    print(request.user)
    return render(request, 'buyevents.html')

def buy_tickets(request):
    return render(request, 'buy_tickets.html')

def credit_card(request):
    print(request.user)
    
    return render(request, 'credit_card.html')

def charge(request):   
    
        amount = 5 
        print('Data', request.POST)
        
        stripe.Customer.create(
            email=request.POST.get('email'),
            name=request.POST.get('name'),
        )
        
        return redirect(reverse('success', args=[amount]))

def ticket(request):
    print(request.user)
    return render(request, 'ticket.html')

@csrf_exempt
def initiate_payment(request):
    if request.method == 'GET':
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        querystring = {"grant_type": "client_credentials"}
        payload = ""
        headers = {
            "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        print(response.text)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    data = response.json()

    access_token = data.get('access_token')
    return access_token

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Only POST requests are allowed"})


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_process(request):

    amount = 1000  

    return render(request, 'payment_process.html', {'amount': amount})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')

def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Virtual Ticket',
                },
                'unit_amount': 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://www.domain.com/payment/success/?redirect=generate_ticket',
        cancel_url='https://www.domain.com/payment/cancel/',
    )

    return redirect(session.url)

def payment_success(request):
    return redirect('generate_ticket')


def generate_ticket(request):
    ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    full_name = request.POST.get('fullName')
    email = request.POST.get('email')

    ticket = Ticket.objects.create(
        full_name=full_name,
        email=email,
        ticket_number=ticket_number,
        ticket_code=ticket_code,
        #ticket.number_of_tickets += 1,
        #tickets.save()
    )

    return render(request, 'ticket_template.html', {'full_name': full_name, 'email': email, 'ticket_number': ticket_number, 'ticket_code': ticket_code})


def create_paypal_payment(request):
    paypal_api_url = 'https://api-m.sandbox.paypal.com/v1/payments/payment'

    client_id = settings.PAYPAL_SANDBOX_CLIENT_ID
    secret = settings.PAYPAL_SANDBOX_SECRET


    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_id}:{secret}'
    }

    data = {
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'transactions': [{
            'amount': {
                'total': '10.00',
                'currency': 'USD'
            }
        }],
        'redirect_urls': {
            'return_url': 'https://eb5b-41-90-184-122.ngrok-free.appv',
            'cancel_url': 'http://localhost:8000/cancel_paypal_payment/'
        }
    }

    response = requests.post(paypal_api_url, headers=headers, json=data)

    if response.status_code == 201:
        payment = response.json()
        approval_url = next(link['href'] for link in payment['links'] if link['rel'] == 'approval_url')
        return HttpResponseRedirect(approval_url)
    else:
        return HttpResponse('Failed to create PayPal payment', status=response.status_code)
