"""
Commande de test pour envoyer des emails d'anniversaire
Usage: 
  - Test rappel (veille): python manage.py test_email_anniversaire --type rappel
  - Test anniversaire (jour même): python manage.py test_email_anniversaire --type anniversaire
  - Test pour un membre spécifique: python manage.py test_email_anniversaire --membre-id 1
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta
from calendrier.models import Membre


class Command(BaseCommand):
    help = 'Test l\'envoi d\'emails d\'anniversaire (rappel ou jour même)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['rappel', 'anniversaire'],
            default='rappel',
            help='Type de test: rappel (veille) ou anniversaire (jour même)'
        )
        parser.add_argument(
            '--membre-id',
            type=int,
            help='ID du membre pour lequel envoyer le test (optionnel)'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Adresse email de test (optionnel, remplace l\'email du membre)'
        )

    def handle(self, *args, **options):
        test_type = options['type']
        membre_id = options.get('membre_id')
        email_test = options.get('email')
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Test Email {test_type.upper()} ===\n'))
        
        # Si un membre spécifique est demandé
        if membre_id:
            try:
                membre = Membre.objects.get(id=membre_id)
                membres = [membre]
            except Membre.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Membre avec ID {membre_id} introuvable.'))
                return
        else:
            # Prendre le premier membre actif avec notifications activées
            membres = Membre.objects.filter(actif=True, notifications_email=True)[:1]
            if not membres.exists():
                self.stdout.write(self.style.ERROR('Aucun membre actif avec notifications activées trouvé.'))
                self.stdout.write(self.style.WARNING('Créez d\'abord un membre dans la gestion.'))
                return
        
        # Déterminer la date selon le type de test
        if test_type == 'rappel':
            # Test rappel = demain (comme la commande normale)
            date_anniversaire = date.today() + timedelta(days=1)
            self.stdout.write('Test RAPPEL (veille de l\'anniversaire)')
            self.stdout.write('   Envoi aux AUTRES membres (pas a l\'anniversaireux)')
            self.stdout.write(f'   Date simulee: {date_anniversaire.strftime("%d/%m/%Y")}\n')
        else:
            # Test anniversaire = aujourd'hui
            date_anniversaire = date.today()
            self.stdout.write('Test ANNIVERSAIRE (jour meme)')
            self.stdout.write('   Envoi a L\'ANNIVERSAIREUX')
            self.stdout.write(f'   Date simulee: {date_anniversaire.strftime("%d/%m/%Y")}\n')
        
        # Envoyer les emails de test
        emails_envoyes = 0
        emails_echoues = 0
        
        for membre in membres:
            try:
                # Préparer le contexte pour l'email
                context = {
                    'membre': membre,
                    'date_anniversaire': date_anniversaire,
                }
                
                # Rendre le template d'email selon le type
                nom_complet = f"{membre.nom} {membre.prenom or ''}".strip()
                
                if test_type == 'rappel':
                    # Email de rappel aux autres membres
                    subject = f'📅 Rappel: Anniversaire de {nom_complet.upper()} demain'
                    html_message = render_to_string('calendrier/email_rappel_anniversaire.html', context)
                    plain_message = f"""
Rappel Anniversaire Demain

Bonsoir famille WOLOKOULO KALEGUELE,

Nous vous rappelons que demain, le {date_anniversaire.strftime('%d/%m/%Y')}, 
nous celebrerons l'anniversaire de {nom_complet.upper()}.

Pionnier du Senang, il est un veritable soldat de la promotion et de la valorisation de la culture senoufo. Son engagement, sa constance et son amour pour nos traditions font de lui un pilier du groupe.

N'oubliez pas de lui souhaiter un joyeux anniversaire demain ! 🎂✨

Le groupe WOLOKOULO KALEGUELE compte sur vous pour celebrer ce moment special.

— Sekongo Kassoum
Premier Responsable des groupes WOLOKOULO KALEGUELE
                    """.strip()
                else:
                    # Email de félicitations à l'anniversaireux
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
                
                # Déterminer l'email de destination
                email_dest = email_test if email_test else membre.email
                
                # Envoyer l'email
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email_dest],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                emails_envoyes += 1
                self.stdout.write(
                    self.style.SUCCESS(f'OK - Email de test envoye a {email_dest}')
                )
                self.stdout.write(f'   Membre: {nom_complet}')
                self.stdout.write(f'   Type: {test_type}')
                self.stdout.write(f'   Date: {date_anniversaire.strftime("%d/%m/%Y")}\n')
                
            except Exception as e:
                emails_echoues += 1
                self.stdout.write(
                    self.style.ERROR(f'ERREUR lors de l\'envoi: {str(e)}')
                )
        
        # Résumé
        self.stdout.write(self.style.SUCCESS(
            f'\n=== Resume ==='
        ))
        self.stdout.write(f'Emails envoyes: {emails_envoyes}')
        if emails_echoues > 0:
            self.stdout.write(self.style.ERROR(f'Echecs: {emails_echoues}'))
        
        if emails_envoyes > 0:
            self.stdout.write(self.style.SUCCESS(
                f'\nOK - Verifiez votre boite de reception: {email_dest if email_test else membre.email}'
            ))

