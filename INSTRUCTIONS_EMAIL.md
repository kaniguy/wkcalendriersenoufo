# Instructions pour configurer Gmail

## ⚠️ Problème d'authentification détecté

L'authentification Gmail a échoué. Voici comment résoudre le problème :

### 1. Vérifier l'authentification à deux facteurs

1. Allez sur https://myaccount.google.com/security
2. Vérifiez que "Validation en deux étapes" est **activée**
3. Si ce n'est pas le cas, activez-la d'abord

### 2. Générer un mot de passe d'application

1. Allez sur https://myaccount.google.com/apppasswords
2. Si vous ne voyez pas cette page, activez d'abord la validation en deux étapes
3. Sélectionnez "Autre (nom personnalisé)" dans le menu déroulant
4. Entrez : `Django Calendrier`
5. Cliquez sur "Générer"
6. **Copiez le mot de passe de 16 caractères** (sans espaces)
7. Utilisez ce mot de passe dans `settings.py` pour `EMAIL_HOST_PASSWORD`

### 3. Vérifier les paramètres dans settings.py

Assurez-vous que les paramètres sont corrects :

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'coullibalyadams02@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-application-16-caracteres'
```

### 4. Tester la configuration

Exécutez le script de test :

```bash
python test_email.py
```

### 5. Alternative : Utiliser OAuth2 (plus sécurisé)

Si vous continuez à avoir des problèmes, vous pouvez utiliser OAuth2 au lieu d'un mot de passe d'application. Cela nécessite l'installation de packages supplémentaires.

## 📧 Configuration actuelle

- **Email** : coullibalyadams02@gmail.com
- **Serveur SMTP** : smtp.gmail.com:587
- **Mot de passe** : uoqhakimofodduvw

**Note** : Le mot de passe fourni semble être un mot de passe d'application, mais il se peut qu'il ne soit plus valide ou qu'il ait été révoqué. Générez-en un nouveau si nécessaire.

