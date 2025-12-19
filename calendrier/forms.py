from django import forms
from .models import SousGroupe, JourCulturel, Partenaire, Membre


class SousGroupeForm(forms.ModelForm):
    class Meta:
        model = SousGroupe
        fields = ['nom', 'description', 'jour_reference', 'actif', 'ordre']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500',
                'rows': 3
            }),
            'jour_reference': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500',
                'type': 'date'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-amber-600 border-gray-300 rounded focus:ring-amber-500'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
        }


class JourCulturelForm(forms.ModelForm):
    class Meta:
        model = JourCulturel
        fields = ['nom', 'ordre', 'sacre']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'sacre': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500'
            }),
        }


class PartenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ['nom', 'logo', 'url', 'actif', 'ordre']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500',
                'placeholder': 'https://example.com'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-amber-600 border-gray-300 rounded focus:ring-amber-500'
            }),
            'ordre': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
        }


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'telephone_whatsapp', 'date_naissance', 'actif', 'notifications_email']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500'
            }),
            'telephone_whatsapp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500',
                'placeholder': '+225XXXXXXXXX'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500',
                'type': 'date'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-amber-600 border-gray-300 rounded focus:ring-amber-500'
            }),
            'notifications_email': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-amber-600 border-gray-300 rounded focus:ring-amber-500'
            }),
        }

