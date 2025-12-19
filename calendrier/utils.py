from datetime import date, timedelta
from .models import SousGroupe, JourCulturel, Membre


def calculer_jour_culturel(date_gregorienne, sous_groupe):
    """
    Calcule le jour culturel sénoufo pour une date grégorienne donnée
    et un sous-groupe spécifique.
    
    Args:
        date_gregorienne: date object
        sous_groupe: instance de SousGroupe
    
    Returns:
        dict avec 'jour' (JourCulturel) et 'numero_jour' (int)
    """
    if not sous_groupe:
        return None
    
    # Récupérer tous les jours culturels du sous-groupe, triés par ordre
    jours = list(sous_groupe.jours_culturels.all().order_by('ordre'))
    
    if not jours:
        return None
    
    # Calculer le nombre de jours entre la date de référence et la date donnée
    jour_reference = sous_groupe.jour_reference
    difference = (date_gregorienne - jour_reference).days
    
    # Calculer l'index dans le cycle (modulo le nombre de jours)
    # Le modulo Python gère correctement les nombres négatifs
    nombre_jours = len(jours)
    index = difference % nombre_jours
    
    # S'assurer que l'index est positif (pour les cas où le modulo pourrait être négatif)
    if index < 0:
        index += nombre_jours
    
    jour_culturel = jours[index]
    
    return {
        'jour': jour_culturel,
        'numero_jour': index + 1,
        'est_sacre': jour_culturel.sacre
    }


def generer_calendrier_mensuel(annee, mois, sous_groupe):
    """
    Génère un calendrier mensuel avec les jours culturels et les anniversaires.
    
    Returns:
        list: Liste de semaines, chaque semaine est une liste de jours
        Chaque jour est un dict avec: date, jour_culturel, est_sacre, est_aujourdhui, anniversaires
    """
    import calendar
    
    # Premier jour du mois
    premier_jour = date(annee, mois, 1)
    
    # Dernier jour du mois
    dernier_jour_num = calendar.monthrange(annee, mois)[1]
    dernier_jour = date(annee, mois, dernier_jour_num)
    
    # Premier jour de la semaine du calendrier (peut être du mois précédent)
    premier_lundi = premier_jour - timedelta(days=premier_jour.weekday())
    
    # Dernier jour de la semaine du calendrier (peut être du mois suivant)
    dernier_dimanche = dernier_jour + timedelta(days=(6 - dernier_jour.weekday()))
    
    # Récupérer tous les membres actifs pour les anniversaires
    membres = Membre.objects.filter(actif=True)
    
    # Créer un dictionnaire des anniversaires par jour du mois
    anniversaires_par_jour = {}
    for membre in membres:
        # Vérifier si l'anniversaire tombe dans ce mois
        if membre.date_naissance.month == mois:
            jour_anniversaire = membre.date_naissance.day
            if jour_anniversaire not in anniversaires_par_jour:
                anniversaires_par_jour[jour_anniversaire] = []
            anniversaires_par_jour[jour_anniversaire].append(membre)
    
    calendrier = []
    semaine = []
    date_courante = premier_lundi
    aujourdhui = date.today()
    
    while date_courante <= dernier_dimanche:
        jour_info = calculer_jour_culturel(date_courante, sous_groupe) if sous_groupe else None
        
        # Récupérer les anniversaires pour ce jour
        anniversaires_du_jour = []
        if date_courante.month == mois and date_courante.day in anniversaires_par_jour:
            anniversaires_du_jour = anniversaires_par_jour[date_courante.day]
        
        jour_data = {
            'date': date_courante,
            'numero': date_courante.day,
            'est_du_mois': date_courante.month == mois,
            'est_aujourdhui': date_courante == aujourdhui,
            'jour_culturel': jour_info['jour'] if jour_info else None,
            'est_sacre': jour_info['est_sacre'] if jour_info else False,
            'anniversaires': anniversaires_du_jour,
        }
        
        semaine.append(jour_data)
        
        # Si on a 7 jours, on passe à la semaine suivante
        if len(semaine) == 7:
            calendrier.append(semaine)
            semaine = []
        
        date_courante += timedelta(days=1)
    
    # Ajouter la dernière semaine si elle n'est pas complète
    if semaine:
        calendrier.append(semaine)
    
    return calendrier

