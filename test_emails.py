"""
Script simple pour tester les emails d'anniversaire
Usage: python test_emails.py
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wolokoulo_kaleguele.settings')
django.setup()

from calendrier.models import Membre

def lister_membres():
    """Liste les membres disponibles pour les tests"""
    membres = Membre.objects.filter(actif=True, notifications_email=True)
    print(f"\n=== Membres disponibles pour les tests ===\n")
    if membres.exists():
        for m in membres:
            nom_complet = f"{m.nom} {m.prenom or ''}".strip()
            print(f"ID: {m.id} - {nom_complet} ({m.email})")
        print(f"\nTotal: {membres.count()} membre(s)")
    else:
        print("Aucun membre actif avec notifications activées.")
        print("\nCréez d'abord un membre dans l'interface de gestion:")
        print("1. Connectez-vous via /connexion/")
        print("2. Allez dans 'Gestion' → 'Membres'")
        print("3. Ajoutez un membre avec notifications activées")
    print()

if __name__ == '__main__':
    lister_membres()
    print("\n=== Commandes de test ===\n")
    print("1. Test RAPPEL (veille):")
    print("   python manage.py test_email_anniversaire --type rappel --email coulibalyadams02@gmail.com")
    print("\n2. Test ANNIVERSAIRE (jour même):")
    print("   python manage.py test_email_anniversaire --type anniversaire --email coulibalyadams02@gmail.com")
    print("\n3. Test pour un membre spécifique:")
    print("   python manage.py test_email_anniversaire --type rappel --membre-id 1")
    print()

