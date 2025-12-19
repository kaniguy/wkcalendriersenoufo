from django.db import models
from django.core.validators import MinValueValidator


class SousGroupe(models.Model):
    """Représente un sous-groupe sénoufo (ex: Tchébara)"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du sous-groupe")
    description = models.TextField(blank=True, verbose_name="Description")
    jour_reference = models.DateField(
        verbose_name="Jour de référence",
        help_text="Date grégorienne servant de point de départ pour le calcul du cycle"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Sous-groupe"
        verbose_name_plural = "Sous-groupes"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class JourCulturel(models.Model):
    """Représente un jour culturel dans le cycle d'un sous-groupe"""
    sous_groupe = models.ForeignKey(
        SousGroupe,
        on_delete=models.CASCADE,
        related_name='jours_culturels',
        verbose_name="Sous-groupe"
    )
    nom = models.CharField(max_length=100, verbose_name="Nom du jour")
    ordre = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Ordre dans le cycle",
        help_text="Position du jour dans le cycle (1, 2, 3, ...)"
    )
    sacre = models.BooleanField(
        default=False,
        verbose_name="Jour sacré/interdit",
        help_text="Si coché, ce jour sera affiché en rouge"
    )
    
    class Meta:
        verbose_name = "Jour culturel"
        verbose_name_plural = "Jours culturels"
        ordering = ['sous_groupe', 'ordre']
        unique_together = [['sous_groupe', 'ordre'], ['sous_groupe', 'nom']]
    
    def __str__(self):
        return f"{self.sous_groupe.nom} - {self.nom}"


class Partenaire(models.Model):
    """Représente un partenaire du Groupe Wolokoulo Kalèguélé"""
    nom = models.CharField(max_length=200, verbose_name="Nom du partenaire")
    logo = models.ImageField(
        upload_to='partenaires/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    url = models.URLField(blank=True, null=True, verbose_name="Site web")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class Membre(models.Model):
    """Représente un membre du Groupe Wolokoulo Kalèguélé"""
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    prenom = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
    email = models.EmailField(verbose_name="Adresse email")
    telephone_whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Numéro WhatsApp",
        help_text="Format: +225XXXXXXXXX"
    )
    date_naissance = models.DateField(verbose_name="Date de naissance")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    notifications_email = models.BooleanField(
        default=True,
        verbose_name="Activer les notifications par email",
        help_text="Recevoir un email la veille de l'anniversaire"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        if self.prenom:
            return f"{self.nom} {self.prenom}"
        return self.nom
    
    def get_age(self):
        """Calcule l'âge du membre"""
        from datetime import date
        today = date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
    
    def get_prochain_anniversaire(self):
        """Retourne la date du prochain anniversaire"""
        from datetime import date
        today = date.today()
        next_birthday = date(today.year, self.date_naissance.month, self.date_naissance.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, self.date_naissance.month, self.date_naissance.day)
        return next_birthday
