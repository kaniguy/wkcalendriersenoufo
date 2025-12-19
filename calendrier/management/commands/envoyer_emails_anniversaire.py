"""
Commande pour envoyer les emails de RAPPEL la veille à 10h00
Usage: python manage.py envoyer_emails_anniversaire

Cette commande envoie un email de RAPPEL à TOUS les autres membres (pas à l'anniversaireux)
pour leur rappeler qu'un anniversaire a lieu demain.
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta
from calendrier.models import Membre


class Command(BaseCommand):
    help = 'Envoie les emails de RAPPEL la veille de l\'anniversaire aux autres membres'

    def handle(self, *args, **options):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        # Trouver les membres dont l'anniversaire est demain
        membres_anniversaire = Membre.objects.filter(
            actif=True,
            notifications_email=True,
            date_naissance__month=tomorrow.month,
            date_naissance__day=tomorrow.day
        )
        
        if not membres_anniversaire.exists():
            self.stdout.write(self.style.SUCCESS('Aucun anniversaire demain.'))
            return
        
        self.stdout.write(f'Trouve {membres_anniversaire.count()} anniversaire(s) demain.')
        
        # Récupérer TOUS les autres membres actifs (pas les anniversaireux)
        autres_membres = Membre.objects.filter(
            actif=True,
            notifications_email=True
        ).exclude(
            id__in=membres_anniversaire.values_list('id', flat=True)
        )
        
        if not autres_membres.exists():
            self.stdout.write(self.style.WARNING('Aucun autre membre pour envoyer les rappels.'))
            return
        
        # Envoyer les emails de rappel à tous les autres membres
        emails_envoyes = 0
        emails_echoues = 0
        
        for membre_anniversaire in membres_anniversaire:
            nom_complet_anniversaire = f"{membre_anniversaire.nom} {membre_anniversaire.prenom or ''}".strip()
            
            # Préparer le contexte pour l'email de rappel
            context = {
                'membre': membre_anniversaire,
                'date_anniversaire': tomorrow,
            }
            
            # Rendre le template d'email de rappel
            subject = f'📅 Rappel: Anniversaire de {nom_complet_anniversaire.upper()} demain'
            html_message = render_to_string('calendrier/email_rappel_anniversaire.html', context)
            plain_message = f"""
Rappel Anniversaire Demain

Bonsoir famille WOLOKOULO KALEGUELE,

Nous vous rappelons que demain, le {tomorrow.strftime('%d/%m/%Y')}, 
nous celebrerons l'anniversaire de {nom_complet_anniversaire.upper()}.

Pionnier du Senang, il est un veritable soldat de la promotion et de la valorisation de la culture senoufo. Son engagement, sa constance et son amour pour nos traditions font de lui un pilier du groupe.

N'oubliez pas de lui souhaiter un joyeux anniversaire demain ! 🎂✨

Le groupe WOLOKOULO KALEGUELE compte sur vous pour celebrer ce moment special.

— Sekongo Kassoum
Premier Responsable des groupes WOLOKOULO KALEGUELE
            """.strip()
            
            # Envoyer l'email de rappel à TOUS les autres membres
            for autre_membre in autres_membres:
                try:
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[autre_membre.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    
                    emails_envoyes += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'OK - Rappel envoye a {autre_membre.email} pour l\'anniversaire de {nom_complet_anniversaire}')
                    )
                    
                except Exception as e:
                    emails_echoues += 1
                    self.stdout.write(
                        self.style.ERROR(f'ERREUR lors de l\'envoi a {autre_membre.email}: {str(e)}')
                    )
        
        # Résumé
        self.stdout.write(self.style.SUCCESS(
            f'\nResume: {emails_envoyes} email(s) de rappel envoye(s), {emails_echoues} echec(s)'
        ))

