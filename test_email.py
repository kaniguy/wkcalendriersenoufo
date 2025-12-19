"""
Script de test pour vérifier la configuration email
Usage: python test_email.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wolokoulo_kaleguele.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test l'envoi d'un email"""
    try:
        print("Test d'envoi d'email...")
        print(f"Email expéditeur: {settings.EMAIL_HOST_USER}")
        print(f"Serveur SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        
        send_mail(
            subject='Test Email - Calendrier Culturel Sénoufo',
            message='Ceci est un email de test pour vérifier la configuration SMTP.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Envoyer à soi-même pour test
            fail_silently=False,
        )
        
        print("OK - Email envoye avec succes!")
        print(f"Verifiez votre boite de reception: {settings.EMAIL_HOST_USER}")
        
    except Exception as e:
        print(f"ERREUR lors de l'envoi: {str(e)}")
        print("\nVerifiez:")
        print("1. Que le mot de passe d'application est correct")
        print("2. Que l'authentification a deux facteurs est activee sur Gmail")
        print("3. Que vous avez genere un mot de passe d'application")
        print("\nPour generer un mot de passe d'application Gmail:")
        print("1. Allez sur https://myaccount.google.com/apppasswords")
        print("2. Selectionnez 'Autre (nom personnalise)' et entrez 'Django Calendrier'")
        print("3. Copiez le mot de passe genere (16 caracteres)")
        print("4. Utilisez ce mot de passe dans EMAIL_HOST_PASSWORD")

if __name__ == '__main__':
    test_email()

