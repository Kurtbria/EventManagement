from django.contrib import admin
from django.urls import path, include
#from paypal.standard.ipn import urls as paypal_urls
#from paypal.standard.ipn.views import ipn
from . import views 

urlpatterns = [
    path('', views.home, name ='home'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('events',views.events,name='events'),
    path('buy_events',views.buy_events,name='buy_events'),
    path('buy_tickets',views.buy_tickets,name='buy_tickets'),
    path('credit_card',views.credit_card,name='credit_card'),
    path('charge/',views.charge,name="charge"),
    #path('success/<str:args>/',views.success_msg,name='successMsg'),
    #path('payment_successful',views.payment_successful,name="payment_successful"),
    #path("payment_cancelled", views.payment_cancelled, namee="payment_cancelled"),
    #path('stripe_webhook',views.stripe_webhook, name="stripe_webhoook"),
    path('ticket',views.ticket,name='ticket'),
    #path('paypal/', include(paypal_urls)),
    #path('paypal/ipn/', ipn, name='paypal-ipn'),
    path('initiate_payment',views.initiate_payment,name='initiate_payment'),
    path('ticket',views.ticket,name='ticket'),
    path('generate_ticket/', views.generate_ticket, name='generate_ticket'),
]
    
    
