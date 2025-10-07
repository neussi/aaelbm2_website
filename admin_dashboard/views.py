from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from main.models import (
    Member, Project, Event, EventRegistration, 
    News, Gallery, Contact, SiteSettings
)
from .forms import (
    ProjectForm, EventForm, NewsForm, GalleryForm, SiteSettingsForm, MemberForm
)

@staff_member_required
def dashboard_home(request):
    """Page d'accueil du dashboard"""
    # Statistiques générales
    stats = {
        'total_members': Member.objects.filter(is_active=True).count(),
        'pending_members': Member.objects.filter(is_active=False).count(),
        'total_projects': Project.objects.count(),
        'ongoing_projects': Project.objects.filter(status='ongoing').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(is_active=True).count(),
        'unread_messages': Contact.objects.filter(is_read=False).count(),
        'total_gallery_items': Gallery.objects.count(),
    }
    
    # Messages récents non lus
    recent_messages = Contact.objects.filter(is_read=False).order_by('-created_at')[:5]
    
    # Événements à venir
    upcoming_events = Event.objects.filter(is_active=True).order_by('date_event')[:5]
    
    # Projets en cours
    ongoing_projects = Project.objects.filter(status='ongoing')[:5]
    
    # Inscriptions récentes aux événements
    recent_registrations = EventRegistration.objects.order_by('-registration_date')[:10]
    
    context = {
        'stats': stats,
        'recent_messages': recent_messages,
        'upcoming_events': upcoming_events,
        'ongoing_projects': ongoing_projects,
        'recent_registrations': recent_registrations,
    }
    
    return render(request, 'admin_dashboard/home.html', context)



# ============= GESTION DES MEMBRES =============

@staff_member_required
def members_list(request):
    """Liste des membres"""
    members = Member.objects.all().order_by('-date_adhesion')
    
    # Filtrage
    member_type = request.GET.get('type')
    search = request.GET.get('search')
    
    if member_type:
        members = members.filter(member_type=member_type)
    
    if search:
        members = members.filter(
            Q(nom_prenom__icontains=search) | 
            Q(email__icontains=search) |
            Q(promotion__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    members_page = paginator.get_page(page_number)
    
    context = {
        'members_page': members_page,
        'member_types': Member.MEMBER_TYPES,
        'current_type': member_type,
        'search_query': search,
    }
    
    return render(request, 'admin_dashboard/members/list.html', context)

@staff_member_required
def member_detail(request, pk):
    """Détail d'un membre"""
    member = get_object_or_404(Member, pk=pk)
    context = {'member': member}
    return render(request, 'admin_dashboard/members/detail.html', context)

@staff_member_required
def member_approve(request, pk):
    """Approuver un membre"""
    member = get_object_or_404(Member, pk=pk)
    member.is_active = True
    member.save()
    messages.success(request, f'Le membre {member.nom_prenom} a été approuvé.')
    return redirect('admin_members_list')

@staff_member_required
def member_reject(request, pk):
    """Rejeter un membre"""
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    messages.success(request, 'La demande d\'adhésion a été rejetée.')
    return redirect('admin_members_list')

# NOUVELLES VUES POUR MEMBRES
@method_decorator(staff_member_required, name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'admin_dashboard/members/form.html'
    success_url = reverse_lazy('admin_members_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Le membre a été créé avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'admin_dashboard/members/form.html'
    success_url = reverse_lazy('admin_members_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Le membre a été modifié avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'admin_dashboard/members/confirm_delete.html'
    success_url = reverse_lazy('admin_members_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Le membre a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# ============= GESTION DES PROJETS =============

@staff_member_required
def projects_list(request):
    """Liste des projets"""
    projects = Project.objects.all().order_by('-created_at')
    
    # Filtrage par statut
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    context = {
        'projects_page': projects_page,
        'status_choices': Project.STATUS_CHOICES,
        'current_status': status,
    }
    
    return render(request, 'admin_dashboard/projects/list.html', context)

@staff_member_required
def project_detail(request, pk):
    """Détail d'un projet"""
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    return render(request, 'admin_dashboard/projects/detail.html', context)

@method_decorator(staff_member_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'admin_dashboard/projects/form.html'
    success_url = reverse_lazy('admin_projects_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Le projet a été créé avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'admin_dashboard/projects/form.html'
    success_url = reverse_lazy('admin_projects_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Le projet a été modifié avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'admin_dashboard/projects/confirm_delete.html'
    success_url = reverse_lazy('admin_projects_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Le projet a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# ============= GESTION DES ÉVÉNEMENTS =============

@staff_member_required
def events_list(request):
    """Liste des événements"""
    events = Event.objects.all().order_by('-date_event')
    
    # Ajouter le nombre d'inscriptions pour chaque événement
    events = events.annotate(registration_count=Count('eventregistration'))
    
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)
    
    context = {'events_page': events_page}
    return render(request, 'admin_dashboard/events/list.html', context)

@method_decorator(staff_member_required, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'admin_dashboard/events/form.html'
    success_url = reverse_lazy('admin_events_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'événement a été créé avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'admin_dashboard/events/form.html'
    success_url = reverse_lazy('admin_events_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'événement a été modifié avec succès.')
        return super().form_valid(form)

# NOUVELLE VUE POUR SUPPRIMER ÉVÉNEMENT
@method_decorator(staff_member_required, name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'admin_dashboard/events/confirm_delete.html'
    success_url = reverse_lazy('admin_events_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'L\'événement a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

@staff_member_required
def event_registrations(request, pk):
    """Liste des inscriptions pour un événement"""
    event = get_object_or_404(Event, pk=pk)
    registrations = event.eventregistration_set.all().order_by('-registration_date')
    
    paginator = Paginator(registrations, 20)
    page_number = request.GET.get('page')
    registrations_page = paginator.get_page(page_number)
    
    context = {
        'event': event,
        'registrations_page': registrations_page,
    }
    
    return render(request, 'admin_dashboard/events/registrations.html', context)

@staff_member_required
def confirm_registration(request, pk):
    """Confirmer une inscription"""
    registration = get_object_or_404(EventRegistration, pk=pk)
    registration.is_confirmed = True
    registration.save()
    
    messages.success(request, f'Inscription de {registration.nom_prenom} confirmée.')
    return redirect('admin_event_registrations', pk=registration.event.pk)

# ============= GESTION DES ACTUALITÉS =============

@staff_member_required
def news_list(request):
    """Liste des actualités"""
    news = News.objects.all().order_by('-created_at')
    
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    context = {'news_page': news_page}
    return render(request, 'admin_dashboard/news/list.html', context)

@method_decorator(staff_member_required, name='dispatch')
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_dashboard/news/form.html'
    success_url = reverse_lazy('admin_news_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'actualité a été créée avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_dashboard/news/form.html'
    success_url = reverse_lazy('admin_news_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'actualité a été modifiée avec succès.')
        return super().form_valid(form)

# NOUVELLE VUE POUR SUPPRIMER ACTUALITÉ
@method_decorator(staff_member_required, name='dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = 'admin_dashboard/news/confirm_delete.html'
    success_url = reverse_lazy('admin_news_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'L\'actualité a été supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# ============= GESTION DE LA GALERIE =============

@staff_member_required
def gallery_list(request):
    """Liste des éléments de galerie"""
    gallery_items = Gallery.objects.all().order_by('-created_at')
    
    # Filtrage par type
    media_type = request.GET.get('type')
    if media_type:
        gallery_items = gallery_items.filter(media_type=media_type)
    
    paginator = Paginator(gallery_items, 12)
    page_number = request.GET.get('page')
    gallery_page = paginator.get_page(page_number)
    
    context = {
        'gallery_page': gallery_page,
        'media_types': Gallery.MEDIA_TYPES,
        'current_type': media_type,
    }
    
    return render(request, 'admin_dashboard/gallery/list.html', context)

@method_decorator(staff_member_required, name='dispatch')
class GalleryCreateView(CreateView):
    model = Gallery
    form_class = GalleryForm
    template_name = 'admin_dashboard/gallery/form.html'
    success_url = reverse_lazy('admin_gallery_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'élément a été ajouté à la galerie avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class GalleryUpdateView(UpdateView):
    model = Gallery
    form_class = GalleryForm
    template_name = 'admin_dashboard/gallery/form.html'
    success_url = reverse_lazy('admin_gallery_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'L\'élément de la galerie a été modifié avec succès.')
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class GalleryDeleteView(DeleteView):
    model = Gallery
    template_name = 'admin_dashboard/gallery/confirm_delete.html'
    success_url = reverse_lazy('admin_gallery_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'L\'élément a été supprimé de la galerie avec succès.')
        return super().delete(request, *args, **kwargs)

# ============= GESTION DES MESSAGES =============

@staff_member_required
def messages_list(request):
    """Liste des messages de contact"""
    messages_list = Contact.objects.all().order_by('-created_at')
    
    # Filtrage
    status = request.GET.get('status')
    if status == 'unread':
        messages_list = messages_list.filter(is_read=False)
    elif status == 'read':
        messages_list = messages_list.filter(is_read=True)
    
    paginator = Paginator(messages_list, 15)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages_page': messages_page,
        'current_status': status,
    }
    
    return render(request, 'admin_dashboard/messages/list.html', context)

@staff_member_required
def message_detail(request, pk):
    """Détail d'un message"""
    message = get_object_or_404(Contact, pk=pk)
    
    # Marquer comme lu
    if not message.is_read:
        message.is_read = True
        message.save()
    
    context = {'message': message}
    return render(request, 'admin_dashboard/messages/detail.html', context)

@staff_member_required
def mark_message_replied(request, pk):
    """Marquer un message comme répondu"""
    message = get_object_or_404(Contact, pk=pk)
    message.is_replied = True
    message.save()
    
    messages.success(request, 'Message marqué comme répondu.')
    return redirect('admin_message_detail', pk=pk)

# NOUVELLE VUE POUR SUPPRIMER MESSAGE
@staff_member_required
def message_delete(request, pk):
    """Supprimer un message"""
    message = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message supprimé avec succès.')
        return redirect('admin_messages_list')
    
    context = {'message': message}
    return render(request, 'admin_dashboard/messages/confirm_delete.html', context)

# ============= PARAMÈTRES DU SITE =============

@staff_member_required
def site_settings(request):
    """Paramètres du site"""
    settings_obj, created = SiteSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paramètres du site mis à jour avec succès.')
            return redirect('admin_site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    
    context = {'form': form}
    return render(request, 'admin_dashboard/settings/form.html', context)