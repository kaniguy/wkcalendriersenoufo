from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from datetime import date, datetime
from .models import SousGroupe, Partenaire, JourCulturel, Membre
from .utils import generer_calendrier_mensuel, calculer_jour_culturel
from .forms import SousGroupeForm, JourCulturelForm, PartenaireForm, MembreForm
import calendar


def calendrier_view(request):
    """Vue principale du calendrier"""
    # Récupérer le sous-groupe sélectionné (depuis GET ou session)
    sous_groupe_id = request.GET.get('sous_groupe')
    
    if sous_groupe_id:
        try:
            sous_groupe = SousGroupe.objects.get(id=sous_groupe_id, actif=True)
            request.session['sous_groupe_id'] = sous_groupe_id
        except SousGroupe.DoesNotExist:
            sous_groupe = None
    else:
        # Récupérer depuis la session ou prendre le premier actif
        sous_groupe_id = request.session.get('sous_groupe_id')
        if sous_groupe_id:
            try:
                sous_groupe = SousGroupe.objects.get(id=sous_groupe_id, actif=True)
            except SousGroupe.DoesNotExist:
                sous_groupe = None
        else:
            sous_groupe = SousGroupe.objects.filter(actif=True).first()
    
    # Récupérer la date sélectionnée (depuis GET) ou utiliser la date actuelle
    date_selection = request.GET.get('date_selection')
    if date_selection:
        try:
            # Parser la date au format YYYY-MM-DD
            date_obj = datetime.strptime(date_selection, '%Y-%m-%d').date()
            annee = date_obj.year
            mois = date_obj.month
        except (ValueError, TypeError):
            annee = date.today().year
            mois = date.today().month
    else:
        # Fallback sur les paramètres annee et mois pour compatibilité
        try:
            annee = int(request.GET.get('annee', date.today().year))
            mois = int(request.GET.get('mois', date.today().month))
        except (ValueError, TypeError):
            annee = date.today().year
            mois = date.today().month
    
    # Valider l'année et le mois
    if not (1 <= mois <= 12):
        mois = date.today().month
    if annee < 1900 or annee > 2100:
        annee = date.today().year
    
    # Générer le calendrier mensuel
    calendrier_mensuel = generer_calendrier_mensuel(annee, mois, sous_groupe)
    
    # Calculer le jour culturel pour aujourd'hui
    jour_aujourdhui = None
    if sous_groupe:
        jour_info = calculer_jour_culturel(date.today(), sous_groupe)
        if jour_info:
            jour_aujourdhui = jour_info['jour']
    
    # Récupérer tous les sous-groupes actifs
    sous_groupes = SousGroupe.objects.filter(actif=True).order_by('ordre', 'nom')
    
    # Récupérer les partenaires actifs
    partenaires = Partenaire.objects.filter(actif=True).order_by('ordre', 'nom')
    
    # Noms des mois en français
    noms_mois = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    
    # Noms des jours de la semaine en français
    noms_jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    
    context = {
        'calendrier_mensuel': calendrier_mensuel,
        'sous_groupes': sous_groupes,
        'sous_groupe_selectionne': sous_groupe,
        'annee': annee,
        'mois': mois,
        'nom_mois': noms_mois[mois - 1],
        'noms_jours': noms_jours,
        'jour_aujourdhui': jour_aujourdhui,
        'date_aujourdhui': date.today(),
        'partenaires': partenaires,
        # Calculer les mois précédent et suivant
        'mois_precedent': mois - 1 if mois > 1 else 12,
        'annee_mois_precedent': annee if mois > 1 else annee - 1,
        'mois_suivant': mois + 1 if mois < 12 else 1,
        'annee_mois_suivant': annee if mois < 12 else annee + 1,
    }
    
    return render(request, 'calendrier/calendrier.html', context)


@csrf_protect
def login_view(request):
    """Vue de connexion personnalisée"""
    if request.user.is_authenticated:
        return redirect('calendrier:gestion')
    
    if request.method == 'POST':
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username}!')
            next_url = request.GET.get('next', 'calendrier:gestion')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm()
    
    return render(request, 'calendrier/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion personnalisée"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('calendrier:calendrier')


@login_required
def gestion_view(request):
    """Tableau de bord de gestion"""
    sous_groupes = SousGroupe.objects.all().order_by('ordre', 'nom')
    partenaires = Partenaire.objects.all().order_by('ordre', 'nom')
    membres = Membre.objects.filter(actif=True).order_by('nom', 'prenom')
    
    context = {
        'sous_groupes': sous_groupes,
        'partenaires': partenaires,
        'membres': membres,
        'total_sous_groupes': sous_groupes.count(),
        'total_partenaires': partenaires.count(),
        'total_membres': membres.count(),
    }
    
    return render(request, 'calendrier/gestion.html', context)


@login_required
def gestion_sous_groupe(request, id=None):
    """Gérer un sous-groupe (créer ou modifier)"""
    if id:
        sous_groupe = get_object_or_404(SousGroupe, id=id)
        action = 'Modifier'
    else:
        sous_groupe = None
        action = 'Créer'
    
    if request.method == 'POST':
        form = SousGroupeForm(request.POST, instance=sous_groupe)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sous-groupe {action.lower()} avec succès!')
            return redirect('calendrier:gestion_sous_groupe_detail', id=form.instance.id)
    else:
        form = SousGroupeForm(instance=sous_groupe)
    
    return render(request, 'calendrier/gestion_sous_groupe.html', {
        'form': form,
        'sous_groupe': sous_groupe,
        'action': action
    })


@login_required
def gestion_sous_groupe_detail(request, id):
    """Détail d'un sous-groupe avec gestion des jours culturels"""
    sous_groupe = get_object_or_404(SousGroupe, id=id)
    jours = sous_groupe.jours_culturels.all().order_by('ordre')
    
    if request.method == 'POST':
        # Gérer la création/modification d'un jour culturel
        jour_id = request.POST.get('jour_id')
        if jour_id:
            jour = get_object_or_404(JourCulturel, id=jour_id, sous_groupe=sous_groupe)
            form = JourCulturelForm(request.POST, instance=jour)
        else:
            form = JourCulturelForm(request.POST)
        
        if form.is_valid():
            jour_culturel = form.save(commit=False)
            jour_culturel.sous_groupe = sous_groupe
            jour_culturel.save()
            messages.success(request, 'Jour culturel enregistré avec succès!')
            return redirect('calendrier:gestion_sous_groupe_detail', id=id)
    else:
        form = JourCulturelForm()
    
    return render(request, 'calendrier/gestion_sous_groupe_detail.html', {
        'sous_groupe': sous_groupe,
        'jours': jours,
        'form': form
    })


@login_required
def gestion_jour_delete(request, id):
    """Supprimer un jour culturel"""
    jour = get_object_or_404(JourCulturel, id=id)
    sous_groupe_id = jour.sous_groupe.id
    jour.delete()
    messages.success(request, 'Jour culturel supprimé avec succès!')
    return redirect('calendrier:gestion_sous_groupe_detail', id=sous_groupe_id)


@login_required
def gestion_partenaire(request, id=None):
    """Gérer un partenaire (créer ou modifier)"""
    if id:
        partenaire = get_object_or_404(Partenaire, id=id)
        action = 'Modifier'
    else:
        partenaire = None
        action = 'Créer'
    
    if request.method == 'POST':
        form = PartenaireForm(request.POST, request.FILES, instance=partenaire)
        if form.is_valid():
            form.save()
            messages.success(request, f'Partenaire {action.lower()} avec succès!')
            return redirect('calendrier:gestion')
    else:
        form = PartenaireForm(instance=partenaire)
    
    return render(request, 'calendrier/gestion_partenaire.html', {
        'form': form,
        'partenaire': partenaire,
        'action': action
    })


@login_required
def gestion_partenaire_delete(request, id):
    """Supprimer un partenaire"""
    partenaire = get_object_or_404(Partenaire, id=id)
    partenaire.delete()
    messages.success(request, 'Partenaire supprimé avec succès!')
    return redirect('calendrier:gestion')


@login_required
def gestion_membre(request, id=None):
    """Gérer un membre (créer ou modifier)"""
    if id:
        membre = get_object_or_404(Membre, id=id)
        action = 'Modifier'
    else:
        membre = None
        action = 'Créer'
    
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, f'Membre {action.lower()} avec succès!')
            return redirect('calendrier:gestion')
    else:
        form = MembreForm(instance=membre)
    
    return render(request, 'calendrier/gestion_membre.html', {
        'form': form,
        'membre': membre,
        'action': action
    })


@login_required
def gestion_membre_delete(request, id):
    """Supprimer un membre"""
    membre = get_object_or_404(Membre, id=id)
    membre.delete()
    messages.success(request, 'Membre supprimé avec succès!')
    return redirect('calendrier:gestion')


@require_http_methods(["GET"])
def export_pdf(request):
    """Export du calendrier en PDF (mensuel ou annuel)"""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from io import BytesIO
        import calendar
        import os
        from django.conf import settings
    except ImportError:
        return HttpResponse(
            "La bibliothèque reportlab n'est pas installée. Installez-la avec: pip install reportlab",
            status=500
        )
    
    # Récupérer les paramètres
    type_export = request.GET.get('type', 'mensuel')  # 'mensuel' ou 'annuel'
    sous_groupe_id = request.GET.get('sous_groupe') or request.session.get('sous_groupe_id')
    try:
        annee = int(request.GET.get('annee', date.today().year))
        mois = int(request.GET.get('mois', date.today().month))
    except (ValueError, TypeError):
        annee = date.today().year
        mois = date.today().month
    
    sous_groupe = None
    if sous_groupe_id:
        try:
            sous_groupe = SousGroupe.objects.get(id=sous_groupe_id, actif=True)
        except SousGroupe.DoesNotExist:
            pass
    
    if not sous_groupe:
        sous_groupe = SousGroupe.objects.filter(actif=True).first()
    
    noms_mois = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    noms_jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    
    # Récupérer les partenaires une seule fois
    partenaires = Partenaire.objects.filter(actif=True).order_by('ordre', 'nom')
    
    # Créer le PDF
    buffer = BytesIO()
    # Ajuster les marges selon le type d'export (plus d'espace en bas pour le footer annuel)
    if type_export == 'annuel':
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                               leftMargin=1*cm, rightMargin=1*cm, 
                               topMargin=1*cm, bottomMargin=4.5*cm)  # Plus d'espace en bas pour le footer agrandi
    else:
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#d97706'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    if type_export == 'annuel':
        # EXPORT ANNUEL - Nouvelle structure avec colonnes verticales
        
        # Fonction pour créer le background avec le logo
        def background_logo(canvas, doc):
            """Dessine le logo en arrière-plan (filigrane) sur chaque page"""
            # Dimensions de la page
            page_width, page_height = landscape(A4)
            
            # Trouver le chemin du logo
            logo_path = None
            if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
                static_dir = settings.STATICFILES_DIRS[0]
                if isinstance(static_dir, (str, bytes)):
                    logo_path = os.path.join(static_dir, 'image', 'logo.png')
                else:
                    logo_path = str(static_dir / 'image' / 'logo.png')
            
            # Si le chemin n'existe pas, essayer le chemin alternatif
            if not (logo_path and os.path.exists(logo_path)):
                from pathlib import Path
                project_root = Path(__file__).resolve().parent.parent.parent
                logo_path = str(project_root / 'static' / 'image' / 'logo.png')
            
            # Dessiner le logo en arrière-plan si il existe
            if logo_path and os.path.exists(logo_path):
                try:
                    from reportlab.lib.utils import ImageReader
                    img = ImageReader(logo_path)
                    img_width, img_height = img.getSize()
                    aspect_ratio = img_width / img_height
                    
                    # Taille du logo en arrière-plan - couvrir toute la page sauf le footer des partenaires
                    # Le footer des partenaires occupe environ 4.5cm en bas (bottomMargin)
                    footer_height = 4.5*cm
                    available_height = page_height - footer_height
                    
                    # Calculer pour que le logo couvre toute la largeur ou toute la hauteur disponible
                    # selon l'aspect ratio
                    if aspect_ratio > (page_width / available_height):
                        # Le logo est plus large que la zone disponible, utiliser la largeur de la page
                        logo_width = page_width
                        logo_height = logo_width / aspect_ratio
                    else:
                        # Le logo est plus haut que la zone disponible, utiliser la hauteur disponible
                        logo_height = available_height
                        logo_width = logo_height * aspect_ratio
                    
                    # Centrer le logo sur la page (hors zone footer)
                    logo_x = (page_width - logo_width) / 2
                    logo_y = footer_height + (available_height - logo_height) / 2
                    
                    # Sauvegarder l'état du canvas
                    canvas.saveState()
                    
                    # Réduire l'opacité pour créer un effet de filigrane discret
                    # Utiliser une opacité faible (0.1 = 10% d'opacité)
                    canvas.setFillAlpha(0.1)  # 10% d'opacité pour un effet très discret
                    canvas.setStrokeAlpha(0.1)
                    
                    # Dessiner le logo centré en arrière-plan avec opacité réduite
                    canvas.drawImage(
                        img, 
                        logo_x, 
                        logo_y, 
                        width=logo_width, 
                        height=logo_height, 
                        preserveAspectRatio=True,
                        mask='auto'  # Préserver la transparence du PNG
                    )
                    
                    # Restaurer l'état du canvas (réinitialise l'opacité)
                    canvas.restoreState()
                except Exception as e:
                    # En cas d'erreur, on continue sans logo
                    pass
        
        # Fonction pour créer le footer avec les partenaires sur chaque page
        def footer_partenaires(canvas, doc):
            """Dessine le footer avec les partenaires sur chaque page"""
            if not partenaires:
                return
            
            # Dimensions de la page
            page_width, page_height = landscape(A4)
            footer_height = 3.5*cm
            footer_y = 1*cm
            
            # Couleur du thème (orange/ambre)
            couleur_theme = colors.HexColor('#d97706')
            couleur_texte = colors.HexColor('#1f2937')  # Gris foncé pour meilleur contraste
            
            # Ligne de séparation avec couleur du thème
            canvas.setStrokeColor(couleur_theme)
            canvas.setLineWidth(1.5)
            canvas.line(1*cm, footer_y + footer_height - 0.3*cm, page_width - 1*cm, footer_y + footer_height - 0.3*cm)
            
            # Titre "Partenaires" - police agrandie et couleur du thème
            canvas.setFont('Helvetica-Bold', 14)
            canvas.setFillColor(couleur_theme)
            canvas.drawCentredString(page_width / 2, footer_y + footer_height - 0.7*cm, "Nos Partenaires")
            
            # Calculer l'espace disponible pour les logos
            available_width = page_width - 2*cm
            num_partenaires = len(partenaires)
            espacement_partenaires = 2.5*cm  # Espacement entre les partenaires
            logo_width = min(2.5*cm, (available_width - (num_partenaires - 1) * espacement_partenaires) / num_partenaires)
            logo_height = 1.2*cm
            
            # Position de départ (centré)
            total_width = num_partenaires * logo_width + (num_partenaires - 1) * espacement_partenaires
            start_x = (page_width - total_width) / 2
            
            # Dessiner les logos et noms des partenaires
            current_x = start_x
            for partenaire in partenaires:
                # Logo si disponible
                if partenaire.logo:
                    try:
                        logo_path = os.path.join(settings.MEDIA_ROOT, str(partenaire.logo))
                        if os.path.exists(logo_path):
                            from reportlab.lib.utils import ImageReader
                            img = ImageReader(logo_path)
                            # Calculer les dimensions en gardant les proportions
                            img_width, img_height = img.getSize()
                            aspect_ratio = img_width / img_height
                            if aspect_ratio > 1:
                                # Image plus large que haute
                                draw_width = logo_width
                                draw_height = logo_width / aspect_ratio
                            else:
                                # Image plus haute que large
                                draw_height = logo_height
                                draw_width = logo_height * aspect_ratio
                            
                            # Centrer l'image
                            img_x = current_x + (logo_width - draw_width) / 2
                            img_y = footer_y + 0.5*cm
                            canvas.drawImage(img, img_x, img_y, width=draw_width, height=draw_height, preserveAspectRatio=True)
                    except Exception as e:
                        pass
                
                # Nom du partenaire - police agrandie et couleur améliorée
                canvas.setFont('Helvetica-Bold', 9)
                canvas.setFillColor(couleur_texte)
                text_y = footer_y + 0.05*cm  # Plus d'espace entre le logo et le nom
                # Tronquer le nom si trop long
                nom = partenaire.nom
                if len(nom) > 25:
                    nom = nom[:22] + "..."
                canvas.drawCentredString(current_x + logo_width / 2, text_y, nom)
                
                current_x += logo_width + espacement_partenaires
        
        # Assigner les fonctions de background et footer au document
        def first_page(canvas, doc):
            background_logo(canvas, doc)  # Logo en arrière-plan
            footer_partenaires(canvas, doc)
        
        def later_pages(canvas, doc):
            background_logo(canvas, doc)  # Logo en arrière-plan
            footer_partenaires(canvas, doc)
        
        doc.onFirstPage = first_page
        doc.onLaterPages = later_pages
        
        # Titre principal
        titre_annuel = Paragraph(
            f"<b>CALENDRIER SÉNOUFO WOLOKOULO KALEGUELE {annee}</b>",
            ParagraphStyle(
                'TitreAnnuel',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.black,
                spaceAfter=10,
                spaceBefore=5,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
        )
        story.append(titre_annuel)
        
        # Sous-titre avec "Wolokoulo Kalèguélé" en grand
        sous_groupe_nom = sous_groupe.nom if sous_groupe else 'Sénoufo'
        sous_titre_annuel = Paragraph(
            f"Sous-groupe sénoufo - {sous_groupe_nom}",
            ParagraphStyle(
                'SousTitreAnnuel',
                parent=styles['Normal'],
                fontSize=16,  # Augmenté de 14 à 16
                textColor=colors.HexColor('#666666'),
                spaceAfter=8,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
        )
        story.append(sous_titre_annuel)
        story.append(Spacer(1, 0.2*cm))
        
        # Fonction pour créer le contenu d'un mois (liste numérotée)
        def creer_liste_mois(annee, mois_num, sous_groupe):
            """Crée une liste numérotée des jours du mois avec format JOUR NUMÉRO – JOUR CULTUREL"""
            calendrier_mensuel = generer_calendrier_mensuel(annee, mois_num, sous_groupe)
            
            # Récupérer tous les jours du mois dans l'ordre
            jours_du_mois = []
            for semaine in calendrier_mensuel:
                for jour in semaine:
                    if jour['est_du_mois']:
                        jours_du_mois.append(jour)
            
            # Créer la liste numérotée avec espacement réduit
            liste_items = []
            for jour in jours_du_mois:
                numero = jour['numero']
                jour_culturel = jour['jour_culturel']
                # Obtenir le nom du jour de la semaine (0 = lundi, 6 = dimanche)
                jour_semaine = jour['date'].weekday()
                nom_jour = noms_jours[jour_semaine]
                
                if jour_culturel:
                    # Format : "15 Mer Koundjène" (avec espace au lieu de tiret)
                    texte = f"{numero} {nom_jour} {jour_culturel.nom}"
                    # Tronquer le nom du jour culturel si trop long
                    if len(texte) > 25:
                        texte = f"{numero} {nom_jour} {jour_culturel.nom[:18]}..."
                    # Style pour les jours sacrés (rouge et gras)
                    if jour['est_sacre']:
                        texte_para = Paragraph(
                            f"<b><font color='red'>{texte}</font></b>",
                            ParagraphStyle(
                                'JourSacré',
                                parent=styles['Normal'],
                                fontSize=7,
                                textColor=colors.red,
                                fontName='Helvetica-Bold',
                                leftIndent=0,
                                spaceAfter=0,
                                leading=11,  # Plus d'espace entre les lignes
                                wordWrap='CJK'  # Permet le retour à la ligne si vraiment nécessaire
                            )
                        )
                    else:
                        texte_para = Paragraph(
                            texte,
                            ParagraphStyle(
                                'JourNormal',
                                parent=styles['Normal'],
                                fontSize=7,
                                textColor=colors.black,
                                leftIndent=0,
                                spaceAfter=0,
                                leading=11,  # Plus d'espace entre les lignes
                                wordWrap='CJK'
                            )
                        )
                    liste_items.append(texte_para)
                else:
                    # Pas de jour culturel
                    texte_para = Paragraph(
                        f"{numero} {nom_jour}",
                        ParagraphStyle(
                            'JourNormal',
                            parent=styles['Normal'],
                            fontSize=7,
                            textColor=colors.grey,
                            leftIndent=0,
                            spaceAfter=0,
                            leading=11  # Plus d'espace entre les lignes
                        )
                    )
                    liste_items.append(texte_para)
            
            return liste_items
        
        # Créer les colonnes : 12 colonnes avec 1 mois chacune
        colonnes_data = []
        
        for mois_num in range(1, 13):
            # En-tête de colonne avec mois uniquement
            couleur_theme = colors.HexColor('#d97706')
            en_tete_col = Paragraph(
                f"<b>{noms_mois[mois_num - 1].upper()}</b>",
                ParagraphStyle(
                    'EnTeteColonne',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.white,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold',
                    spaceAfter=1,
                    leading=11
                )
            )
            
            # Liste des jours pour le mois
            liste_jours = creer_liste_mois(annee, mois_num, sous_groupe)
            
            # Créer le contenu de la colonne
            contenu_colonne = [[en_tete_col]]
            contenu_colonne.extend([[item] for item in liste_jours])
            
            # Créer le tableau de la colonne avec hauteurs minimales
            colonne_table = Table(contenu_colonne, colWidths=[3.8*cm])
            colonne_table.setStyle(TableStyle([
                # En-tête avec fond orange et texte blanc
                ('BACKGROUND', (0, 0), (0, 0), couleur_theme),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
                # Ligne de séparation sous l'en-tête
                ('LINEBELOW', (0, 0), (0, 0), 1.5, colors.white),
                # Bordures subtiles autour de la colonne
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),  # Gris très clair
                # Fond alterné très doux pour améliorer la lisibilité
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),  # Blanc et gris très clair
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            colonnes_data.append([colonne_table])
        
        # Créer la grille avec 12 colonnes (diviser en 2 pages : 6 colonnes par page)
        # Page 1 : 6 premiers mois (Janvier à Juin)
        grille_page1 = [colonnes_data[0:6]]
        grille_table_page1 = Table(grille_page1, colWidths=[3.8*cm]*6)
        grille_table_page1.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        
        story.append(grille_table_page1)
        story.append(PageBreak())
        
        # Page 2 : 6 derniers mois (Juillet à Décembre)
        grille_page2 = [colonnes_data[6:12]]
        grille_table_page2 = Table(grille_page2, colWidths=[3.8*cm]*6)
        grille_table_page2.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        
        story.append(grille_table_page2)
        
        nom_fichier = f"calendrier_annuel_{sous_groupe.nom if sous_groupe else 'senoufo'}_{annee}.pdf"
        
    else:
        # EXPORT MENSUEL - Une page
        # Titre principal
        titre = Paragraph(
            f"Calendrier Culturel Sénoufo - {sous_groupe.nom if sous_groupe else 'Groupe Wolokoulo Kalèguélé'}",
            titre_style
        )
        story.append(titre)
        
        calendrier_mensuel = generer_calendrier_mensuel(annee, mois, sous_groupe)
        
        # Mois et année
        sous_titre = Paragraph(
            f"{noms_mois[mois - 1]} {annee}",
            styles['Heading2']
        )
        story.append(sous_titre)
        story.append(Spacer(1, 0.5*cm))
        
        # Tableau du calendrier
        data = [noms_jours]  # En-tête
        
        for semaine in calendrier_mensuel:
            ligne = []
            for jour in semaine:
                if jour['est_du_mois']:
                    texte = f"{jour['numero']}\n"
                    if jour['jour_culturel']:
                        texte += jour['jour_culturel'].nom
                    if jour['anniversaires']:
                        for membre in jour['anniversaires']:
                            texte += f"\n🎂 {membre.nom}"
                    if not jour['jour_culturel'] and not jour['anniversaires']:
                        texte += "-"
                else:
                    texte = ""
                ligne.append(texte)
            data.append(ligne)
        
        # Créer le tableau
        table = Table(data, colWidths=[3*cm]*7, rowHeights=[1*cm]*len(data))
        
        # Style du tableau
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Colorier les jours sacrés en rouge
        ligne_num = 1
        for semaine in calendrier_mensuel:
            col_num = 0
            for jour in semaine:
                if jour['est_du_mois'] and jour['est_sacre']:
                    table_style.add('TEXTCOLOR', (col_num, ligne_num), (col_num, ligne_num), colors.red)
                    table_style.add('FONTNAME', (col_num, ligne_num), (col_num, ligne_num), 'Helvetica-Bold')
                col_num += 1
            ligne_num += 1
        
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 1*cm))
        
        # Footer avec partenaires (logo + nom) - uniquement pour PDF mensuel
        if partenaires:
            story.append(Spacer(1, 0.5*cm))
            
            # Ligne de séparation
            story.append(Spacer(1, 0.3*cm))
            ligne_separation = Table([['']], colWidths=[landscape(A4)[0] - 2*cm])
            ligne_separation.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (0, 0), 1, colors.grey),
            ]))
            story.append(ligne_separation)
            story.append(Spacer(1, 0.3*cm))
            
            # Titre partenaires
            titre_partenaires = Paragraph(
                "<b>Partenaires</b>",
                ParagraphStyle(
                    'TitrePartenaires',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.black,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold',
                    spaceAfter=10
                )
            )
            story.append(titre_partenaires)
            
            # Créer un tableau pour les logos et noms des partenaires
            partenaires_cellules = []
            for partenaire in partenaires:
                # Créer une cellule avec logo (si disponible) et nom
                contenu_cellule = []
                
                # Logo si disponible
                if partenaire.logo:
                    try:
                        logo_path = os.path.join(settings.MEDIA_ROOT, str(partenaire.logo))
                        if os.path.exists(logo_path):
                            logo_img = Image(logo_path, width=2*cm, height=1.5*cm)
                            contenu_cellule.append(logo_img)
                    except:
                        pass
                
                # Nom du partenaire
                nom_para = Paragraph(
                    partenaire.nom,
                    ParagraphStyle(
                        'NomPartenaire',
                        parent=styles['Normal'],
                        fontSize=9,
                        textColor=colors.black,
                        alignment=TA_CENTER,
                        spaceAfter=0
                    )
                )
                contenu_cellule.append(nom_para)
                
                # Créer un tableau vertical pour cette cellule (logo au-dessus, nom en dessous)
                cellule_table = Table([[item] for item in contenu_cellule], colWidths=[3*cm])
                cellule_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                partenaires_cellules.append([cellule_table])
            
            # Organiser les partenaires en ligne (maximum 4 par ligne)
            if partenaires_cellules:
                partenaires_table_data = []
                cellule_vide = Paragraph('', styles['Normal'])  # Cellule vide avec Paragraph
                for i in range(0, len(partenaires_cellules), 4):
                    ligne = partenaires_cellules[i:i+4]
                    # Compléter avec des cellules vides si nécessaire
                    while len(ligne) < 4:
                        ligne.append([cellule_vide])
                    partenaires_table_data.append(ligne)
                
                partenaires_table = Table(partenaires_table_data, colWidths=[4.5*cm]*4)
                partenaires_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(partenaires_table)
        
        nom_fichier = f"calendrier_{sous_groupe.nom if sous_groupe else 'senoufo'}_{mois}_{annee}.pdf"
    
    # Générer le PDF
    doc.build(story)
    
    # Récupérer le PDF
    pdf = buffer.getvalue()
    buffer.close()
    
    # Réponse HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
    response.write(pdf)
    
    return response
