from django.contrib import admin
from .models import SousGroupe, JourCulturel, Partenaire, Membre


class JourCulturelInline(admin.TabularInline):
    """Inline pour gérer les jours culturels depuis le sous-groupe"""
    model = JourCulturel
    extra = 1
    ordering = ['ordre']
    fields = ['nom', 'ordre', 'sacre']


@admin.register(SousGroupe)
class SousGroupeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre', 'actif', 'nombre_jours']
    list_filter = ['actif']
    search_fields = ['nom', 'description']
    ordering = ['ordre', 'nom']
    inlines = [JourCulturelInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'ordre', 'actif')
        }),
        ('Configuration du cycle', {
            'fields': ('jour_reference',),
            'description': 'La date de référence sert de point de départ pour le calcul du cycle des jours culturels.'
        }),
    )
    
    def nombre_jours(self, obj):
        """Affiche le nombre de jours culturels du sous-groupe"""
        return obj.jours_culturels.count()
    nombre_jours.short_description = "Nombre de jours"


@admin.register(JourCulturel)
class JourCulturelAdmin(admin.ModelAdmin):
    list_display = ['nom', 'sous_groupe', 'ordre', 'sacre']
    list_filter = ['sous_groupe', 'sacre']
    search_fields = ['nom', 'sous_groupe__nom']
    ordering = ['sous_groupe', 'ordre']
    
    fieldsets = (
        ('Informations', {
            'fields': ('sous_groupe', 'nom', 'ordre')
        }),
        ('Caractéristiques', {
            'fields': ('sacre',),
            'description': 'Les jours sacrés sont affichés en rouge dans le calendrier.'
        }),
    )


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre', 'actif', 'a_logo']
    list_filter = ['actif']
    search_fields = ['nom']
    ordering = ['ordre', 'nom']
    
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'url', 'ordre', 'actif')
        }),
        ('Logo', {
            'fields': ('logo',),
            'description': 'Le logo apparaîtra dans le footer du calendrier.'
        }),
    )
    
    def a_logo(self, obj):
        """Indique si le partenaire a un logo"""
        return "Oui" if obj.logo else "Non"
    a_logo.short_description = "A un logo"
    a_logo.boolean = True


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'email', 'telephone_whatsapp', 'date_naissance', 'actif', 'notifications_email']
    list_filter = ['actif', 'notifications_email']
    search_fields = ['nom', 'prenom', 'email', 'telephone_whatsapp']
    ordering = ['nom', 'prenom']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance')
        }),
        ('Coordonnées', {
            'fields': ('email', 'telephone_whatsapp')
        }),
        ('Paramètres', {
            'fields': ('actif', 'notifications_email')
        }),
    )
    
    def nom_complet(self, obj):
        """Retourne le nom complet"""
        if obj.prenom:
            return f"{obj.nom} {obj.prenom}"
        return obj.nom
    nom_complet.short_description = "Nom complet"
