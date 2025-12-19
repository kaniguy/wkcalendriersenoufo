"""
Commande pour envoyer les emails le JOUR MÊME de l'anniversaire
Usage: python manage.py envoyer_emails_jour_anniversaire

Cette commande envoie un email de FÉLICITATIONS à l'anniversaireux le jour de son anniversaire.
Cette commande doit être exécutée quotidiennement via un cron job à 10h00
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
from calendrier.models import Membre


class Command(BaseCommand):
    help = 'Envoie les emails de FELICITATIONS le jour meme de l\'anniversaire a l\'anniversaireux'

    def handle(self, *args, **options):
        today = date.today()
        
        # Trouver les membres dont l'anniversaire est AUJOURD'HUI
        membres_anniversaire = Membre.objects.filter(
            actif=True,
            notifications_email=True,
            date_naissance__month=today.month,
            date_naissance__day=today.day
        )
        
        if not membres_anniversaire.exists():
            self.stdout.write(self.style.SUCCESS('Aucun anniversaire aujourd\'hui.'))
            return
        
        self.stdout.write(f'Trouve {membres_anniversaire.count()} anniversaire(s) aujourd\'hui.')
        
        # Envoyer les emails de félicitations aux anniversaireux
        emails_envoyes = 0
        emails_echoues = 0
        
        for membre in membres_anniversaire:
            try:
                # Préparer le contexte pour l'email
                context = {
                    'membre': membre,
                    'date_anniversaire': today,
                }
                
                # Rendre le template d'email
                nom_complet = f"{membre.nom} {membre.prenom or ''}".strip()
                subject = f'🎉 JOYEUX ANNIVERSAIRE {nom_complet.upper()} ! 🎉'
                html_message = render_to_string('calendrier/email_jour_anniversaire.html', context)
                plain_message = f"""
JOYEUX ANNIVERSAIRE !

Bonjour {nom_complet},

🎂 Le groupe WOLOKOULO KALEGUELE te souhaite un tres joyeux anniversaire ! 🎂

En ce jour special, nous celebrons ta personne et ton engagement exceptionnel dans la promotion et la valorisation de la culture senoufo.

Pionnier du Senang, tu es un veritable soldat de notre cause. Ton engagement, ta constance et ton amour pour nos traditions font de toi un pilier du groupe.

Nous te souhaitons sante, longevite, reussite et beaucoup de force pour continuer ce noble combat culturel.

Joyeux anniversaire {nom_complet} ! 🎂✨

Le groupe WOLOKOULO KALEGUELE est fier de toi et te remercie pour tout ce que tu apportes a notre communaute.

— Sekongo Kassoum
Premier Responsable des groupes WOLOKOULO KALEGUELE
                """.strip()
                
                # Envoyer l'email à l'anniversaireux
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[membre.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                emails_envoyes += 1
                self.stdout.write(
                    self.style.SUCCESS(f'OK - Email de felicitations envoye a {membre.email} ({nom_complet})')
                )
                
            except Exception as e:
                emails_echoues += 1
                self.stdout.write(
                    self.style.ERROR(f'ERREUR lors de l\'envoi a {membre.email}: {str(e)}')
                )
        
        # Résumé
        self.stdout.write(self.style.SUCCESS(
            f'\nResume: {emails_envoyes} email(s) de felicitations envoye(s), {emails_echoues} echec(s)'
        ))
