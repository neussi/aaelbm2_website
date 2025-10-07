from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone

class Member(models.Model):
    """Modèle pour les membres de l'association"""
    MEMBER_TYPES = [
        ('founder', 'Membre Fondateur'),
        ('bureau', 'Membre du Bureau'),
        ('conseil', 'Conseiller'),
        ('simple', 'Membre Simple'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prénom")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    promotion = models.CharField(max_length=20, verbose_name="Promotion (année de sortie)")
    telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    email = models.EmailField(verbose_name="Adresse e-mail")
    profession = models.CharField(max_length=200, verbose_name="Profession actuelle")
    adresse = models.TextField(verbose_name="Adresse actuelle")
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPES, default='simple')
    poste_bureau = models.CharField(max_length=100, blank=True, null=True, verbose_name="Poste au bureau")
    photo = models.ImageField(upload_to='members/', blank=True, null=True)
    bio = RichTextField(blank=True, null=True, verbose_name="Biographie")
    is_active = models.BooleanField(default=False)
    date_adhesion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['nom_prenom']
    
    def __str__(self):
        return self.nom_prenom

class Project(models.Model):
    """Modèle pour les projets de l'association"""
    STATUS_CHOICES = [
        ('planning', 'En planification'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminé'),
        ('suspended', 'Suspendu'),
    ]
    
    title_fr = models.CharField(max_length=200, verbose_name="Titre (Français)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (Anglais)")
    description_fr = RichTextField(verbose_name="Description (Français)")
    description_en = RichTextField(verbose_name="Description (Anglais)")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    budget_required = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Budget requis (FCFA)")
    budget_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Budget collecté (FCFA)")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    is_featured = models.BooleanField(default=False, verbose_name="Projet en vedette")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_fr
    
    @property
    def progress_percentage(self):
        if self.budget_required > 0:
            return min((self.budget_collected / self.budget_required) * 100, 100)
        return 0

class Event(models.Model):
    """Modèle pour les événements"""
    title_fr = models.CharField(max_length=200, verbose_name="Titre (Français)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (Anglais)")
    description_fr = RichTextField(verbose_name="Description (Français)")
    description_en = RichTextField(verbose_name="Description (Anglais)")
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date_event = models.DateTimeField(verbose_name="Date et heure de l'événement")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    max_participants = models.IntegerField(blank=True, null=True, verbose_name="Nombre maximum de participants")
    registration_deadline = models.DateTimeField(verbose_name="Date limite d'inscription")
    is_featured = models.BooleanField(default=False, verbose_name="Événement en vedette")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['date_event']
    
    def __str__(self):
        return self.title_fr
    
    @property
    def is_registration_open(self):
        return timezone.now() < self.registration_deadline and self.is_active
    
    @property
    def registered_count(self):
        return self.eventregistration_set.filter(is_confirmed=True).count()

class EventRegistration(models.Model):
    """Modèle pour les inscriptions aux événements"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prénom")
    email = models.EmailField(verbose_name="Adresse e-mail")
    telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    promotion = models.CharField(max_length=20, verbose_name="Promotion")
    message = models.TextField(blank=True, verbose_name="Message/Commentaire")
    is_confirmed = models.BooleanField(default=False, verbose_name="Confirmé")
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Inscription à l'événement"
        verbose_name_plural = "Inscriptions aux événements"
        unique_together = ['event', 'email']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.nom_prenom} - {self.event.title_fr}"

class News(models.Model):
    """Modèle pour les actualités"""
    title_fr = models.CharField(max_length=200, verbose_name="Titre (Français)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (Anglais)")
    content_fr = RichTextField(verbose_name="Contenu (Français)")
    content_en = RichTextField(verbose_name="Contenu (Anglais)")
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Publié")
    is_featured = models.BooleanField(default=False, verbose_name="Article en vedette")
    publication_date = models.DateTimeField(verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-publication_date']
    
    def __str__(self):
        return self.title_fr

class Gallery(models.Model):
    """Modèle pour la galerie multimédia"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]
    
    title_fr = models.CharField(max_length=200, verbose_name="Titre (Français)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (Anglais)")
    description_fr = models.TextField(blank=True, verbose_name="Description (Français)")
    description_en = models.TextField(blank=True, verbose_name="Description (Anglais)")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, verbose_name="URL de la vidéo")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, verbose_name="En vedette")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Élément de galerie"
        verbose_name_plural = "Galerie"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_fr

class Contact(models.Model):
    """Modèle pour les messages de contact"""
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prénom")
    email = models.EmailField(verbose_name="Adresse e-mail")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    is_replied = models.BooleanField(default=False, verbose_name="Répondu")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nom_prenom} - {self.sujet}"

class SiteSettings(models.Model):
    """Paramètres du site"""
    site_name = models.CharField(max_length=200, default="A²ELBM2")
    slogan_fr = models.CharField(max_length=300, verbose_name="Slogan (Français)")
    slogan_en = models.CharField(max_length=300, verbose_name="Slogan (Anglais)")
    description_fr = RichTextField(verbose_name="Description de l'association (Français)")
    description_en = RichTextField(verbose_name="Description de l'association (Anglais)")
    president_message_fr = RichTextField(verbose_name="Message du président (Français)")
    president_message_en = RichTextField(verbose_name="Message du président (Anglais)")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    facebook_url = models.URLField(blank=True)
    whatsapp_group_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"
    
    def __str__(self):
        return self.site_name