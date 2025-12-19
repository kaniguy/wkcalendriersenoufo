from django.urls import path
from . import views

app_name = 'calendrier'

urlpatterns = [
    path('', views.calendrier_view, name='calendrier'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    # Authentification
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    # Gestion
    path('gestion/', views.gestion_view, name='gestion'),
    path('gestion/sous-groupe/', views.gestion_sous_groupe, name='gestion_sous_groupe'),
    path('gestion/sous-groupe/<int:id>/', views.gestion_sous_groupe, name='gestion_sous_groupe_edit'),
    path('gestion/sous-groupe/<int:id>/detail/', views.gestion_sous_groupe_detail, name='gestion_sous_groupe_detail'),
    path('gestion/jour/<int:id>/supprimer/', views.gestion_jour_delete, name='gestion_jour_delete'),
    path('gestion/partenaire/', views.gestion_partenaire, name='gestion_partenaire'),
    path('gestion/partenaire/<int:id>/', views.gestion_partenaire, name='gestion_partenaire_edit'),
    path('gestion/partenaire/<int:id>/supprimer/', views.gestion_partenaire_delete, name='gestion_partenaire_delete'),
    # Membres
    path('gestion/membre/', views.gestion_membre, name='gestion_membre'),
    path('gestion/membre/<int:id>/', views.gestion_membre, name='gestion_membre_edit'),
    path('gestion/membre/<int:id>/supprimer/', views.gestion_membre_delete, name='gestion_membre_delete'),
]

