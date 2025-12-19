from .models import Partenaire


def partenaires(request):
    """Context processor pour rendre les partenaires disponibles dans tous les templates"""
    return {
        'partenaires': Partenaire.objects.filter(actif=True).order_by('ordre', 'nom')
    }

