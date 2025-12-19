# Calendrier Culturel Sénoufo - Groupe Wolokoulo Kalèguélé

Application web de calendrier culturel sénoufo permettant de consulter et de valoriser les jours culturels des différents sous-groupes sénoufo.

## 🌍 Caractéristiques

- **Accès public** : Le calendrier est accessible sans connexion
- **Gestion des sous-groupes** : Chaque sous-groupe possède son propre système de jours culturels
- **Calendrier culturel** : Affichage des jours culturels sénoufo basé sur le calendrier grégorien
- **Export PDF** : Fonctionnalité d'export du calendrier en PDF
- **Gestion des partenaires** : Affichage des partenaires dans le footer
- **Interface moderne** : Design sobre avec Tailwind CSS

## 🚀 Installation

### Prérequis

- Python 3.11+
- Django 5.2+

### Étapes d'installation

1. **Activer l'environnement virtuel** (déjà créé dans `mon_env/`)
   ```bash
   # Sur Windows
   mon_env\Scripts\activate
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

4. **Créer un superutilisateur** (pour accéder à l'administration)
   ```bash
   python manage.py createsuperuser
   ```

5. **Initialiser les données de base** (sous-groupe Tchébara)
   ```bash
   python manage.py init_data
   ```

6. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Calendrier : http://127.0.0.1:8000/
   - Administration : http://127.0.0.1:8000/admin/

## 📖 Utilisation

### Gestion des membres et anniversaires

L'application permet de gérer les membres du groupe avec leurs dates de naissance. Les emails d'anniversaire sont envoyés automatiquement la veille à 10h00.

**Pour configurer l'envoi automatique d'emails :**
1. Configurez les paramètres email dans `settings.py` (voir `CONFIGURATION_EMAIL.md`)
2. Configurez un cron job ou une tâche planifiée pour exécuter quotidiennement à 10h00 :
   ```bash
   python manage.py envoyer_emails_anniversaire
   ```

Voir le fichier `CONFIGURATION_EMAIL.md` pour plus de détails.

### Consultation du calendrier

1. Accédez à la page d'accueil
2. Sélectionnez un sous-groupe dans la liste déroulante
3. Naviguez entre les mois avec les boutons "Précédent" et "Suivant"
4. Les jours sacrés sont affichés en rouge

### Administration

L'interface d'administration permet de :

- **Gérer les sous-groupes** :
  - Ajouter/modifier des sous-groupes
  - Définir le jour de référence (point de départ du cycle)
  - Activer/désactiver des sous-groupes

- **Gérer les jours culturels** :
  - Définir la liste des jours pour chaque sous-groupe
  - Définir l'ordre des jours dans le cycle
  - Marquer les jours sacrés/interdits (affichés en rouge)

- **Gérer les partenaires** :
  - Ajouter des partenaires avec logo
  - Définir l'ordre d'affichage
  - Activer/désactiver des partenaires

- **Gérer les membres** :
  - Ajouter/modifier des membres
  - Enregistrer nom, email, numéro WhatsApp, date de naissance
  - Activer/désactiver les notifications d'anniversaire par email
  - Les emails sont envoyés automatiquement la veille de l'anniversaire à 10h00

### Export PDF

Cliquez sur le bouton "Exporter en PDF" pour télécharger le calendrier du mois en cours au format PDF.

## 🧩 Structure des données

### Sous-groupe Tchébara (exemple)

Cycle de 6 jours :
1. N'KPA
2. Tôri
3. Wagounou
4. Tchôgninh
5. Koundjène (jour sacré - affiché en rouge)
6. Kakpôhô

Le jour de référence (19 décembre 2025) correspond au jour N'KPA.

## 🛠️ Technologies utilisées

- **Django** : Framework web Python
- **Tailwind CSS** : Framework CSS pour le design
- **ReportLab** : Génération de PDF
- **Pillow** : Traitement d'images pour les logos des partenaires
- **SMTP** : Envoi d'emails pour les notifications d'anniversaire

## 📝 Notes

- Le calendrier est entièrement public, aucune connexion n'est requise pour le consulter
- La connexion est uniquement nécessaire pour l'administration
- Chaque sous-groupe peut avoir un nombre variable de jours dans son cycle
- Le calcul des jours culturels se base sur le jour de référence défini pour chaque sous-groupe
- Les emails d'anniversaire sont envoyés automatiquement la veille à 10h00 via une tâche planifiée

## 👥 Groupe Wolokoulo Kalèguélé

Application créée pour la valorisation et la promotion de la culture sénoufo.

