from django.contrib import admin
from django.urls import path, include
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
    path('ticket',views.ticket,name='ticket'),
    path('create_checkout_session',views.create_checkout_session,name='create_checkout_session'),
    path('initiate_payment',views.initiate_payment,name='initiate_payment'),
    path('ticket',views.ticket,name='ticket'),
    path('generate_ticket/', views.generate_ticket, name='generate_ticket'),
    path('create_paypal_payment',views.create_paypal_payment,name='create_paypal_payment'),
    path('signout',views.signout,name='signout')
]
    
    
