import stripe
import requests
import random
import string
import io, re, os
import datetime
import base64
from django.views.generic import View
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
#from .paypal_client import PayPalClient
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

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
    
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')


def signout(request):
    logout(request)

    return redirect('home')  

def events(request):
    print(request.user)
    
    return render(request, 'events.html', {'events': events})

def list_events(request):
    print(request.user)
    return render(request, 'list_events.html')

def buy_tickets(request):
    return render(request, 'buy_tickets.html')

def credit_card(request):
    print(request.user)
    
    return render(request, 'credit_card.html')

def charge(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        try:
            charge = stripe.Charge.create(
                amount=1000,  
                currency='usd',
                description='Event Payment',
                source=token,
            )
            
            return render(request, 'charge_success.html')
        except stripe.error.CardError as e:
            
            return render(request, 'charge_error.html', {'error': e})
    else:
       
        return render(request, 'credit_card.html')

def charge_success(request):
    return render(request, 'charge_success.html')

def charge_error(request):
    return render(request, 'charge_error.html')


def ticket(request):
    print(request.user)
    return render(request, 'ticket.html')

@csrf_exempt
def initiate_payment(request):
  if request.method == 'POST':
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
    querystring = {"grant_type": "client_credentials"}
    payload = ""
    headers = {
      "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
    }
    response = requests.request("POST", url, headers=headers, params=querystring)
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


def payment_process(request):

    amount = 1000  

    return render(request, 'payment_process.html', {'amount': amount})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')




def payment_success(request):
    return redirect('generate_ticket')


@login_required
def generate_ticket(request):
  if request.method == 'POST':
    ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    full_name = request.POST.get('fullName')
    email = request.POST.get('email')

    if full_name:
      purchase_datetime = timezone.now()

      # Create Ticket object
      ticket = Ticket.objects.create(
          full_name=full_name,
          email=email,
          ticket_number=ticket_number,
          ticket_code=ticket_code,
          date=purchase_datetime,
      )

      return render(request, 'ticket_template.html', {
          'full_name': full_name,
          'email': email,
          'ticket_number': ticket_number,
          'ticket_code': ticket_code,
          'purchase_datetime': purchase_datetime
      })
    else:
      error_message = "Full name is required."
      return redirect('buy_tickets.html', {'error_message': error_message})
  else:
    error_message = "Invalid request method."
    return render(request, 'buy_tickets.html', {'error_message': error_message})


@require_POST
@login_required
def create_paypal_payment(request):
  paypal_api_url = 'https://api-m.sandbox.paypal.com/v1/payments/payment'

  client_id = settings.PAYPAL_SANDBOX_CLIENT_ID
  secret = settings.PAYPAL_SANDBOX_SECRET

  credentials = base64.b64encode(f"{client_id}:{secret}".encode('utf-8')).decode('utf-8')
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {credentials}'
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
      'return_url': '#',
      'cancel_url': '#'
    }
  }

  response = requests.post(paypal_api_url, headers=headers, json=data)

  if response.status_code == 201:
    payment = response.json()
    approval_url = next(link['href'] for link in payment['links'] if link['rel'] == 'approval_url')
    return HttpResponseRedirect(approval_url)
  else:
    error_message = f"Failed to create PayPal payment. Status code: {response.status_code}"
    if response.text:
      error_message += f"\nError details: {response.text}"
    return HttpResponseBadRequest(error_message)


@login_required
def user_privilage(request):
    if request.user.is_superuser:
        return JsonResponse({'message': 'You are a privileged user.'})
    elif request.user.is_staff:
        if request.user.has_perm('your_app_name.can_access_privileged_feature'):
            return JsonResponse({'message': 'You have access to the privileged feature.'})
        else:
            return JsonResponse({'message': 'You do not have access to the privileged feature.'}, status=403)
    else:
        return JsonResponse({'message': 'You do not have sufficient privileges.'}, status=403)


def email_pattern(email):

    email_pattern = r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+(?:[a-zA-Z]{2,})$'
    
    if not re.match(email_pattern, email):
        return False

    if email.endswith('@gmail.com') or email.endswith('@googlemail.com'):
        return True
    else:
        return False 


@csrf_exempt
def create_order(request):
    url = 'https://api.sandbox.paypal.com/v2/checkout/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)


    if response.status_code == 201:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({'error': 'Failed to create order'}, status=500)

def get_access_token():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    data = {
        'grant_type': 'client_credentials'
    }
    auth = (os.environ.get('PAYPAL_CLIENT_ID'), os.environ.get('PAYPAL_CLIENT_SECRET'))
    response = requests.post(url, data=data, auth=auth)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

def checkout(request):
    print(request.user)

    return render(request, 'checkout.html')

def stripe_checkout(request):
    if request.method == 'POST':
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Virtual Ticket',
                        },
                        'unit_amount': 100,  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',

                success_url=request.build_absolute_uri(reverse('payment_success')),
                cancel_url=request.build_absolute_uri(reverse('payment_cancel'))
            )
            return redirect(session.url, code=303)
        except Exception as e:
            print(e)
            return redirect(reverse('error_page'))
    else:
        return redirect(reverse('home'))

