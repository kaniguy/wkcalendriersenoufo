# Guide de Test des Emails d'Anniversaire

## 📧 Commandes de Test Disponibles

### 1. Test Email RAPPEL (veille de l'anniversaire)

Cette commande simule l'envoi d'un email la veille de l'anniversaire (comme la commande automatique) :

```bash
python manage.py test_email_anniversaire --type rappel
```

**Options supplémentaires :**
- `--membre-id X` : Tester pour un membre spécifique (ID)
- `--email votre-email@example.com` : Envoyer à une adresse email différente

**Exemples :**
```bash
# Test rappel pour le premier membre actif
python manage.py test_email_anniversaire --type rappel

# Test rappel pour un membre spécifique
python manage.py test_email_anniversaire --type rappel --membre-id 1

# Test rappel vers votre email personnel
python manage.py test_email_anniversaire --type rappel --email coulibalyadams02@gmail.com
```

### 2. Test Email ANNIVERSAIRE (jour même)

Cette commande simule l'envoi d'un email le jour de l'anniversaire :

```bash
python manage.py test_email_anniversaire --type anniversaire
```

**Exemples :**
```bash
# Test anniversaire pour le premier membre actif
python manage.py test_email_anniversaire --type anniversaire

# Test anniversaire pour un membre spécifique
python manage.py test_email_anniversaire --type anniversaire --membre-id 1

# Test anniversaire vers votre email personnel
python manage.py test_email_anniversaire --type anniversaire --email coulibalyadams02@gmail.com
```

## 📋 Étapes pour Tester

### Étape 1 : Vérifier qu'il y a des membres

1. Connectez-vous à l'interface de gestion : `/connexion/`
2. Allez dans "Gestion" → Section "Membres"
3. Vérifiez qu'il y a au moins un membre avec :
   - `Actif` = ✓
   - `Notifications email` = ✓
   - Une adresse email valide

### Étape 2 : Tester le rappel (veille)

```bash
python manage.py test_email_anniversaire --type rappel --email coulibalyadams02@gmail.com
```

### Étape 3 : Tester l'anniversaire (jour même)

```bash
python manage.py test_email_anniversaire --type anniversaire --email coulibalyadams02@gmail.com
```

## 🔍 Vérifier les Membres Disponibles

Pour voir la liste des membres et leurs IDs :

```bash
python manage.py shell
```

Puis dans le shell :
```python
from calendrier.models import Membre
membres = Membre.objects.filter(actif=True, notifications_email=True)
for m in membres:
    print(f"ID: {m.id} - {m.nom} {m.prenom or ''} ({m.email})")
```

## ⚠️ Notes Importantes

- Les tests utilisent le même template que les emails automatiques
- Vous pouvez envoyer les tests à votre propre email pour vérifier le rendu
- Les tests ne dépendent pas de la date réelle de naissance des membres
- Assurez-vous que la configuration email est correcte dans `settings.py`

## 🎯 Commandes Automatiques (Production)

Une fois les tests validés, configurez la tâche planifiée pour l'envoi automatique :

**Rappel (veille) - 10h00 :**
```bash
python manage.py envoyer_emails_anniversaire
```

Cette commande est celle qui sera exécutée automatiquement chaque jour à 10h00.

