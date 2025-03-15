import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tesla_lagacy.settings')  # Adjust this to your project name
django.setup()

# Test sending an email
try:
    send_mail(
        'Test Subject',
        'Test Message',
        settings.EMAIL_HOST_USER,  # Use the email from your settings
        ['yakubudestiny9@gmail.com'],  # Replace with a valid recipient email
        fail_silently=False,
    )
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")