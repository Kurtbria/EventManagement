from django.contrib import admin
from django.urls import path, include
from . import views 
#from eventmanagement.views import SigninView 
urlpatterns = [
    path('', views.home, name ='home'),
    path('user_signup',views.user_signup, name='user_signup'),
    #path('signin/', SigninView.as_view(), name='signin'),
    path('user_signin',views.user_signin,name='user_signin'),
    path('events',views.events,name='events'),
    path('list_events',views.list_events,name='list_events'),
    path('buy_tickets',views.buy_tickets,name='buy_tickets'),
    path('credit_card',views.credit_card,name='credit_card'),
    path('ticket',views.ticket,name='ticket'),
    path('stripe_checkout',views.stripe_checkout,name='stripe_checkout'),
    path('initiate_payment',views.initiate_payment,name='initiate_payment'),
    path('ticket',views.ticket,name='ticket'),
    path('generate_ticket/', views.generate_ticket, name='generate_ticket'),
    path('create_paypal_payment',views.create_paypal_payment,name='create_paypal_payment'),
    path('signout',views.signout,name='signout'),
    path('user_privilage',views.user_privilage,name='user_privilage'),
    path('email_pattern',views.email_pattern,name='email_pattern'),
    path('charge',views.charge,name='charge'),
    path('charge/success/', views.charge_success, name='charge_success'),
    path('charge/error/', views.charge_error, name='charge_error'),
    path('create_order',views.create_order, name='create_order'),
    path('checkout',views.checkout,name='checkout'),
    path('list_users',views.list_users,name='list_users'),
    #path('rear_view', views.rear_view,name='rear_view'),

]

