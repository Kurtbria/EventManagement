from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_welcome_email(email):
    subject = 'Welcome to EMS !!'
    message = render_to_string('welcome_email.html')
    sender_email = 'j.ericndivo@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)