import stripe
import requests
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

# M-Pesa API credentials
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
SHORTCODE = 'your_shortcode'
PASSKEY = 'your_passkey'
INITIATE_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least eight characters')
            return redirect('signup')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.') 
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('signup')
            
        myuser = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('login')
    else:
        return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  

    return render(request, 'login.html')

def home(request):
    print(request.user)
    return render(request, 'base.html')

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
    if request.method == 'POST':
        amount = 5 
        print('Data', request.POST)
        
        stripe.Customer.create(
            email=request.POST.get('email'),
            name=request.POST.get('name'),
        )
        
        return redirect(reverse('success', args=[amount]))

def success_msg(request, args):
    amount = args
    return render(request, 'base.success.html', {'amount': amount})

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
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        print(response.text)
        # Process the response and return appropriate JSON response
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
        # Process M-Pesa callback notification
        # Update transaction status in your database
        # You can use a background task processing library like Celery to handle this asynchronously
        # Respond to Safaricom server with HTTP status 200 to acknowledge receipt of the notification
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Only POST requests are allowed"})


'''
def payment_process(request):
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '10.00',
        'currency_code': 'USD',
        'item_name': 'Virtual Ticket',
        'invoice': 'unique-invoice-id',
        'notify_url': 'https://yourdomain.com/paypal/ipn/',  
        'return_url': 'https://yourdomain.com/payment/success/',
        'cancel_return': 'https://yourdomain.com/payment/cancel/',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment_process.html', {'form': form})

@csrf_exempt
def payment_success(request):
    return HttpResponse("Payment Successful")

@csrf_exempt
def payment_cancel(request):
    return HttpResponse("Payment Canceled")
'''



def generate_ticket(request):
    # Generate a unique ticket number and code
    ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    # Get form data
    full_name = request.POST.get('fullName')
    email = request.POST.get('email')

    # Render the ticket template with the generated data
    return render(request, 'ticket_template.html', {'full_name': full_name, 'email': email, 'ticket_number': ticket_number, 'ticket_code': ticket_code})
