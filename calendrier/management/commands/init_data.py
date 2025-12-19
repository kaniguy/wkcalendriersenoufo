"""
Commande pour initialiser les données de base
Usage: python manage.py init_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from calendrier.models import SousGroupe, JourCulturel


class Command(BaseCommand):
    help = 'Initialise les données de base (sous-groupe Tchébara avec ses jours culturels)'

    def handle(self, *args, **options):
        self.stdout.write('Création des données initiales...')
        
        # Créer le sous-groupe Tchébara
        tchebara, created = SousGroupe.objects.get_or_create(
            nom='Tchébara',
            defaults={
                'description': 'Sous-groupe sénoufo Tchébara',
                'jour_reference': date(2025, 12, 19),  # Vendredi 19 décembre 2025 = N'KPA
                'actif': True,
                'ordre': 1
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Sous-groupe "{tchebara.nom}" créé.'))
        else:
            self.stdout.write(f'Sous-groupe "{tchebara.nom}" existe déjà.')
        
        # Créer les jours culturels pour Tchébara
        jours_tchebara = [
            ('N\'KPA', 1, False),
            ('Tôri', 2, False),
            ('Wagounou', 3, False),
            ('Tchôgninh', 4, False),
            ('Koundjène', 5, True),  # Jour sacré
            ('Kakpôhô', 6, False),
        ]
        
        for nom, ordre, sacre in jours_tchebara:
            jour, created = JourCulturel.objects.get_or_create(
                sous_groupe=tchebara,
                nom=nom,
                defaults={
                    'ordre': ordre,
                    'sacre': sacre
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Jour "{nom}" créé.'))
            else:
                self.stdout.write(f'  Jour "{nom}" existe déjà.')
        
        self.stdout.write(self.style.SUCCESS('\nDonnées initiales créées avec succès!'))

