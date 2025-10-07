from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Member, Project, Event, EventRegistration, 
    News, Gallery, Contact, SiteSettings
)
from .forms import (
    MemberRegistrationForm, EventRegistrationForm, 
    ContactForm
)

def home(request):
    """Page d'accueil"""
    # Récupérer les paramètres du site
    site_settings = SiteSettings.objects.first()
    
    # Événements en vedette (prochains)
    featured_events = Event.objects.filter(
        is_featured=True,
        is_active=True,
        date_event__gte=timezone.now()
    )[:3]
    
    # Projets en vedette
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    
    # Actualités récentes
    recent_news = News.objects.filter(is_published=True)[:4]
    
    # Galerie en vedette
    featured_gallery = Gallery.objects.filter(is_featured=True)[:6]
    
    # Membres du bureau
    bureau_members = Member.objects.filter(
        is_active=True
    )
    
    context = {
        'site_settings': site_settings,
        'featured_events': featured_events,
        'featured_projects': featured_projects,
        'recent_news': recent_news,
        'featured_gallery': featured_gallery,
        'bureau_members': bureau_members,
    }
    
    return render(request, 'main/home.html', context)

def about(request):
    """Page à propos"""
    site_settings = SiteSettings.objects.first()
    
    # Statistiques
    total_members = Member.objects.filter(is_active=True).count()
    completed_projects = Project.objects.filter(status='completed').count()
    ongoing_projects = Project.objects.filter(status='ongoing').count()
    
    context = {
        'site_settings': site_settings,
        'total_members': total_members,
        'completed_projects': completed_projects,
        'ongoing_projects': ongoing_projects,
    }
    
    return render(request, 'main/about.html', context)

def members(request):
    """Page des membres"""
    # Membres du bureau
    bureau_members = Member.objects.filter(
        member_type='bureau',
        is_active=True
    ).order_by('poste_bureau')
    
    # Membres fondateurs
    founder_members = Member.objects.filter(
        member_type='founder',
        is_active=True
    )
    
    # Conseillers
    conseil_members = Member.objects.filter(
        member_type='conseil',
        is_active=True
    )
    general_members = Member.objects.filter(
        is_active=True
    )
    # Membres influents (avec bio)
    influential_members = Member.objects.filter(
        is_active=True,
        bio__isnull=False
    ).exclude(bio='')[:8]
    
    context = {
        'bureau_members': bureau_members,
        'founder_members': founder_members,
        'conseil_members': conseil_members,
        'influential_members': influential_members,
        'general_members': general_members,

    }
    
    return render(request, 'main/members.html', context)



def member_registration(request):
    """Inscription d'un nouveau membre"""
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)  # Ajouter request.FILES
        if form.is_valid():
            member = form.save(commit=False)
            member.is_active = False  # En attente de validation par l'administration
            member.save()
            
            messages.success(
                request, 
                _('Votre demande d\'adhésion a été envoyée avec succès! '
                  'Vous recevrez une confirmation par email une fois votre compte validé.')
            )
            
            # Envoyer un email de notification à l'administration
            try:
                # Email pour l'administration
                admin_subject = 'Nouvelle demande d\'adhésion - A²ELBM2'
                admin_message = f"""
                Nouvelle demande d'adhésion reçue:
                
                Nom et Prénom: {member.nom_prenom}
                Email: {member.email}
                Téléphone: {member.telephone}
                Promotion: {member.promotion}
                Profession: {member.profession}
                Lieu de naissance: {member.lieu_naissance}
                Date de naissance: {member.date_naissance}
                Adresse actuelle: {member.adresse}
                Photo: {'Oui' if member.photo else 'Non'}
                
                Veuillez vous connecter à l'administration pour valider ou rejeter cette demande.
                """
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.EMAIL_HOST_USER,
                    [settings.ASSOCIATION_EMAIL],
                    fail_silently=True,
                )
                
                # Email de confirmation pour le membre
                member_subject = 'Demande d\'adhésion reçue - A²ELBM2'
                member_message = f"""
                Bonjour {member.nom_prenom},
                
                Nous avons bien reçu votre demande d'adhésion à l'Association des Anciens Élèves 
                du Lycée Bilingue de Melong 2 (A²ELBM2).
                
                Votre demande sera examinée par notre bureau dans un délai de 48 heures.
                Vous recevrez une confirmation par email une fois votre adhésion validée.
                
                Récapitulatif de votre demande:
                - Promotion: {member.promotion}
                - Email: {member.email}
                - Téléphone: {member.telephone}
                
                En cas de questions, n'hésitez pas à nous contacter.
                
                Cordialement,
                L'équipe A²ELBM2
                """
                
                send_mail(
                    member_subject,
                    member_message,
                    settings.EMAIL_HOST_USER,
                    [member.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Logger l'erreur mais ne pas bloquer l'inscription
                print(f"Erreur lors de l'envoi de l'email: {e}")
                pass
            
            return redirect('member_registration_success')
    else:
        form = MemberRegistrationForm()
    
    context = {
        'form': form,
        'page_title': _('Devenir membre'),
    }
    return render(request, 'main/member_registration.html', context)


def member_registration_success(request):
    """Page de confirmation après inscription"""
    context = {
        'page_title': _('Demande envoyée'),
    }
    return render(request, 'main/member_registration_success.html', context)

    

def projects(request):
    """Page des projets"""
    # Projets en cours
    ongoing_projects = Project.objects.filter(status='ongoing')
    
    # Projets terminés
    completed_projects = Project.objects.filter(status='completed')
    
    # Projets en planification
    planning_projects = Project.objects.filter(status='planning')
    
    context = {
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'planning_projects': planning_projects,
    }
    
    return render(request, 'main/projects.html', context)

def project_detail(request, pk):
    """Détail d'un projet"""
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    return render(request, 'main/project_detail.html', context)

def events(request):
    """Page des événements"""
    # Événements à venir
    upcoming_events = Event.objects.filter(
        date_event__gte=timezone.now(),
        is_active=True
    ).order_by('date_event')
    
    # Événements passés
    past_events = Event.objects.filter(
        date_event__lt=timezone.now()
    ).order_by('-date_event')[:6]
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    
    return render(request, 'main/events.html', context)

def event_detail(request, pk):
    """Détail d'un événement"""
    event = get_object_or_404(Event, pk=pk)
    
    # Vérifier si l'inscription est ouverte
    can_register = event.is_registration_open
    
    if request.method == 'POST' and can_register:
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            
            # Vérifier si pas déjà inscrit
            existing = EventRegistration.objects.filter(
                event=event,
                email=registration.email
            ).first()
            
            if existing:
                messages.warning(request, _('Vous êtes déjà inscrit à cet événement.'))
            else:
                registration.save()
                messages.success(request, _('Votre inscription a été enregistrée avec succès!'))
                
                # Envoyer notification
                try:
                    send_mail(
                        f'Nouvelle inscription - {event.title_fr}',
                        f'Participant: {registration.nom_prenom}\nEmail: {registration.email}',
                        settings.EMAIL_HOST_USER,
                        [settings.ASSOCIATION_EMAIL],
                        fail_silently=True,
                    )
                except:
                    pass
                
                return redirect('event_registration_success', pk=event.pk)
    else:
        form = EventRegistrationForm()
    
    context = {
        'event': event,
        'form': form,
        'can_register': can_register,
    }
    
    return render(request, 'main/event_detail.html', context)

def event_registration_success(request, pk):
    """Page de confirmation d'inscription à un événement"""
    event = get_object_or_404(Event, pk=pk)
    context = {'event': event}
    return render(request, 'main/event_registration_success.html', context)

def news(request):
    """Page des actualités"""
    news_list = News.objects.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(news_list, 9)
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    context = {'news_page': news_page}
    return render(request, 'main/news.html', context)

def news_detail(request, pk):
    """Détail d'une actualité"""
    article = get_object_or_404(News, pk=pk, is_published=True)
    
    # Articles connexes
    related_news = News.objects.filter(
        is_published=True
    ).exclude(pk=pk)[:3]
    
    context = {
        'article': article,
        'related_news': related_news,
    }
    
    return render(request, 'main/news_detail.html', context)

def gallery(request):
    """Page de la galerie"""
    # Images
    images = Gallery.objects.filter(media_type='image').order_by('-created_at')
    
    # Vidéos
    videos = Gallery.objects.filter(media_type='video').order_by('-created_at')
    
    context = {
        'images': images,
        'videos': videos,
    }
    
    return render(request, 'main/gallery.html', context)

def donations(request):
    """Page des dons et cotisations"""
    # Projets nécessitant des fonds
    funded_projects = Project.objects.filter(
        status__in=['planning', 'ongoing']
    ).order_by('-is_featured', '-created_at')
    
    context = {
        'funded_projects': funded_projects,
        'whatsapp_president': settings.WHATSAPP_PRESIDENT,
        'whatsapp_treasurer_mtn': settings.WHATSAPP_TREASURER_MTN,
        'whatsapp_treasurer_orange': settings.WHATSAPP_TREASURER_ORANGE,
    }
    
    return render(request, 'main/donations.html', context)

def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            messages.success(request, _('Votre message a été envoyé avec succès! Nous vous répondrons bientôt.'))
            
            # Envoyer notification par email
            try:
                send_mail(
                    f'Nouveau message de contact - {contact_message.sujet}',
                    f'De: {contact_message.nom_prenom} ({contact_message.email})\n\nMessage:\n{contact_message.message}',
                    settings.EMAIL_HOST_USER,
                    [settings.ASSOCIATION_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'main/contact.html', context)

def contact_success(request):
    """Page de confirmation de contact"""
    return render(request, 'main/contact_success.html')

@csrf_exempt
def whatsapp_redirect(request):
    """Redirection vers WhatsApp"""
    contact_type = request.GET.get('type', 'president')
    message = request.GET.get('message', '')
    
    if contact_type == 'president':
        phone = settings.WHATSAPP_PRESIDENT
    elif contact_type == 'treasurer_mtn':
        phone = settings.WHATSAPP_TREASURER_MTN
    elif contact_type == 'treasurer_orange':
        phone = settings.WHATSAPP_TREASURER_ORANGE
    else:
        phone = settings.WHATSAPP_PRESIDENT
    
    # Nettoyer le numéro de téléphone
    phone = phone.replace('+', '').replace(' ', '').replace('-', '')
    
    whatsapp_url = f"https://wa.me/{phone}"
    if message:
        whatsapp_url += f"?text={message}"
    
    return redirect(whatsapp_url)

def handler404(request, exception=None):
    """Page d'erreur 404 personnalisée"""
    context = {
        'error_code': '404',
        'error_title': 'Page non trouvée',
        'error_message': 'Désolé, la page que vous recherchez n\'existe pas ou a été déplacée.',
    }
    return render(request, 'errors/404.html', context, status=404)


def handler500(request):
    """Page d'erreur 500 personnalisée"""
    context = {
        'error_code': '500',
        'error_title': 'Erreur serveur',
        'error_message': 'Une erreur interne s\'est produite. Notre équipe technique a été notifiée et travaille à résoudre le problème.',
    }
    return render(request, 'errors/500.html', context, status=500)

