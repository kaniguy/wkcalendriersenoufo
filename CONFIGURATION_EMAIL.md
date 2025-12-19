# Configuration de l'envoi automatique d'emails d'anniversaire

## 📧 Configuration Email

### 1. Configuration dans settings.py

Modifiez les paramètres suivants dans `wolokoulo_kaleguele/settings.py` :

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Ou votre fournisseur (smtp.outlook.com, etc.)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-application'
DEFAULT_FROM_EMAIL = 'Groupe Wolokoulo Kalèguélé <votre-email@gmail.com>'
```

### 2. Pour Gmail

1. Activez l'authentification à deux facteurs sur votre compte Gmail
2. Générez un "Mot de passe d'application" :
   - Allez dans : https://myaccount.google.com/apppasswords
   - Sélectionnez "Autre (nom personnalisé)" et entrez "Django Calendrier"
   - Copiez le mot de passe généré (16 caractères)
   - Utilisez ce mot de passe dans `EMAIL_HOST_PASSWORD`

### 3. Pour Outlook/Hotmail

```python
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@outlook.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe'
```

## ⏰ Configuration du Cron Job (Envoi automatique à 10h00)

### Sur Linux/Mac

Ajoutez cette ligne dans votre crontab (`crontab -e`) :

```bash
0 10 * * * cd /chemin/vers/votre/projet && /chemin/vers/python manage.py envoyer_emails_anniversaire
```

Exemple :
```bash
0 10 * * * cd /home/user/wolokoulo-kaleguele && /usr/bin/python3 manage.py envoyer_emails_anniversaire
```

### Sur Windows (Task Scheduler)

1. Ouvrez le "Planificateur de tâches" (Task Scheduler)
2. Créez une tâche de base
3. Définissez :
   - **Déclencheur** : Quotidien à 10:00
   - **Action** : Démarrer un programme
   - **Programme** : `C:\chemin\vers\mon_env\Scripts\python.exe`
   - **Arguments** : `manage.py envoyer_emails_anniversaire`
   - **Répertoire de départ** : `E:\DOSSIER ADAMS\DJANGO\WOLOKOULO KALEGUELE`

### Test manuel

Pour tester l'envoi d'emails manuellement :

```bash
python manage.py envoyer_emails_anniversaire
```

## 📝 Notes importantes

- Les emails sont envoyés **la veille** de l'anniversaire à **10h00**
- Seuls les membres avec `actif=True` et `notifications_email=True` recevront des emails
- Assurez-vous que le serveur est accessible à 10h00 pour exécuter la commande
- Vérifiez les logs pour s'assurer que les emails sont bien envoyés

## 🔍 Vérification

Pour vérifier qu'un membre recevra un email demain :

```python
from datetime import date, timedelta
from calendrier.models import Membre

tomorrow = date.today() + timedelta(days=1)
membres = Membre.objects.filter(
    actif=True,
    notifications_email=True,
    date_naissance__month=tomorrow.month,
    date_naissance__day=tomorrow.day
)
print(f"Membres avec anniversaire demain: {membres.count()}")
for m in membres:
    print(f"- {m.nom} ({m.email})")
```

