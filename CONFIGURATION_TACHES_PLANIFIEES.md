# Configuration des Tâches Planifiées - Emails d'Anniversaire

## 📧 Système d'Emails en Deux Étapes

Votre système envoie maintenant **deux types d'emails** :

### 1. 📅 Email de RAPPEL (la veille à 10h00)
- **Destinataires** : TOUS les autres membres (pas l'anniversaireux)
- **Objectif** : Rappeler aux membres qu'un anniversaire a lieu demain
- **Commande** : `python manage.py envoyer_emails_anniversaire`

### 2. 🎉 Email de FÉLICITATIONS (le jour même à 10h00)
- **Destinataire** : L'ANNIVERSAIREUX uniquement
- **Objectif** : Souhaiter joyeux anniversaire à la personne concernée
- **Commande** : `python manage.py envoyer_emails_jour_anniversaire`

## ⚙️ Configuration Windows Task Scheduler

Vous devez créer **DEUX tâches planifiées** qui s'exécutent chaque jour à 10h00.

### Tâche 1 : Rappel (veille)

1. **Ouvrir le Planificateur de tâches** (`taskschd.msc`)

2. **Créer une tâche de base** nommée : `Rappel Anniversaire - Wolokoulo`

3. **Déclencheur** :
   - Type : Quotidien
   - Heure : 10:00
   - Répéter : Chaque jour

4. **Action** :
   - Action : Démarrer un programme
   - Programme : `E:\DOSSIER ADAMS\DJANGO\WOLOKOULO KALEGUELE\mon_env\Scripts\python.exe`
   - Arguments : `manage.py envoyer_emails_anniversaire`
   - Répertoire de départ : `E:\DOSSIER ADAMS\DJANGO\WOLOKOULO KALEGUELE`

5. **Conditions** :
   - ✅ Démarrer la tâche même si l'ordinateur est alimenté par batterie
   - ✅ Réveiller l'ordinateur pour exécuter cette tâche (optionnel)

### Tâche 2 : Félicitations (jour même)

1. **Créer une deuxième tâche** nommée : `Felicitations Anniversaire - Wolokoulo`

2. **Déclencheur** :
   - Type : Quotidien
   - Heure : 10:00 (même heure)
   - Répéter : Chaque jour

3. **Action** :
   - Action : Démarrer un programme
   - Programme : `E:\DOSSIER ADAMS\DJANGO\WOLOKOULO KALEGUELE\mon_env\Scripts\python.exe`
   - Arguments : `manage.py envoyer_emails_jour_anniversaire`
   - Répertoire de départ : `E:\DOSSIER ADAMS\DJANGO\WOLOKOULO KALEGUELE`

4. **Conditions** : Identiques à la tâche 1

## 🧪 Tests

### Tester le rappel (veille)
```bash
python manage.py envoyer_emails_anniversaire
```
**Résultat attendu** : Emails envoyés à TOUS les autres membres (pas à l'anniversaireux)

### Tester les félicitations (jour même)
```bash
python manage.py envoyer_emails_jour_anniversaire
```
**Résultat attendu** : Email envoyé à l'anniversaireux uniquement

### Tests avec la commande de test
```bash
# Test rappel
python manage.py test_email_anniversaire --type rappel --email coulibalyadams02@gmail.com

# Test félicitations
python manage.py test_email_anniversaire --type anniversaire --email coulibalyadams02@gmail.com
```

## 📋 Exemple de Fonctionnement

### Scénario : Anniversaire le 20 décembre

**Le 19 décembre à 10h00** :
- ✅ Tâche 1 s'exécute : `envoyer_emails_anniversaire`
- ✅ Emails de RAPPEL envoyés à tous les membres SAUF celui qui a son anniversaire le 20
- 📧 Les membres reçoivent : "Rappel: Anniversaire de [NOM] demain"

**Le 20 décembre à 10h00** :
- ✅ Tâche 2 s'exécute : `envoyer_emails_jour_anniversaire`
- ✅ Email de FÉLICITATIONS envoyé à l'anniversaireux uniquement
- 📧 L'anniversaireux reçoit : "🎉 JOYEUX ANNIVERSAIRE [NOM] ! 🎉"

## ⚠️ Points Importants

1. **Les deux tâches s'exécutent à la même heure (10h00)**
   - C'est normal, elles vérifient des dates différentes (demain vs aujourd'hui)

2. **Ordre d'exécution**
   - Les deux tâches peuvent s'exécuter en parallèle
   - Aucun problème si elles s'exécutent en même temps

3. **Si plusieurs anniversaires le même jour**
   - Rappel : Tous les autres membres reçoivent un email pour chaque anniversaire
   - Félicitations : Chaque anniversaireux reçoit son email personnel

## 🔍 Vérification

Pour vérifier que les tâches fonctionnent :

1. **Vérifier l'historique dans le Planificateur de tâches**
2. **Tester manuellement les deux commandes**
3. **Vérifier les boîtes de réception des membres**

## 📝 Commandes Utiles

```bash
# Rappel (veille) - aux autres membres
python manage.py envoyer_emails_anniversaire

# Félicitations (jour même) - à l'anniversaireux
python manage.py envoyer_emails_jour_anniversaire

# Tests
python manage.py test_email_anniversaire --type rappel --email votre-email@gmail.com
python manage.py test_email_anniversaire --type anniversaire --email votre-email@gmail.com
```

