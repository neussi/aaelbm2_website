# admin_dashboard/urls.py - Fichier principal mis à jour
from django.urls import path, include
from . import views
from . import auth_views

urlpatterns = [
    # ============= AUTHENTIFICATION =============
    # Pages d'authentification
    path('auth/login/', auth_views.admin_login_view, name='admin_login'),
    path('auth/logout/', auth_views.admin_logout_view, name='admin_logout'),
    path('auth/register/', auth_views.admin_register_view, name='admin_register'),
    path('auth/password-reset/', auth_views.admin_password_reset_view, name='admin_password_reset'),
    
    # ============= DASHBOARD =============
    # Dashboard home (nécessite une connexion)
    path('', views.dashboard_home, name='admin_dashboard_home'),
    
    # ============= GESTION DES MEMBRES =============
    path('members/', views.members_list, name='admin_members_list'),
    path('members/create/', views.MemberCreateView.as_view(), name='admin_member_create'),
    path('members/<int:pk>/', views.member_detail, name='admin_member_detail'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='admin_member_edit'),
    path('members/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='admin_member_delete'),
    path('members/<int:pk>/approve/', views.member_approve, name='admin_member_approve'),
    path('members/<int:pk>/reject/', views.member_reject, name='admin_member_reject'),
    
    # ============= GESTION DES PROJETS =============
    path('projects/', views.projects_list, name='admin_projects_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='admin_project_create'),
    path('projects/<int:pk>/', views.project_detail, name='admin_project_detail'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='admin_project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='admin_project_delete'),
    
    # ============= GESTION DES ÉVÉNEMENTS =============
    path('events/', views.events_list, name='admin_events_list'),
    path('events/create/', views.EventCreateView.as_view(), name='admin_event_create'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='admin_event_edit'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='admin_event_delete'),
    path('events/<int:pk>/registrations/', views.event_registrations, name='admin_event_registrations'),
    path('registrations/<int:pk>/confirm/', views.confirm_registration, name='admin_confirm_registration'),
    
    # ============= GESTION DES ACTUALITÉS =============
    path('news/', views.news_list, name='admin_news_list'),
    path('news/create/', views.NewsCreateView.as_view(), name='admin_news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='admin_news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='admin_news_delete'),
    
    # ============= GESTION DE LA GALERIE =============
    path('gallery/', views.gallery_list, name='admin_gallery_list'),
    path('gallery/create/', views.GalleryCreateView.as_view(), name='admin_gallery_create'),
    path('gallery/<int:pk>/edit/', views.GalleryUpdateView.as_view(), name='admin_gallery_edit'),
    path('gallery/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='admin_gallery_delete'),
    
    # ============= GESTION DES MESSAGES =============
    path('messages/', views.messages_list, name='admin_messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='admin_message_detail'),
    path('messages/<int:pk>/reply/', views.mark_message_replied, name='admin_mark_message_replied'),
    path('messages/<int:pk>/delete/', views.message_delete, name='admin_message_delete'),
    
    # ============= PARAMÈTRES DU SITE =============
    path('settings/', views.site_settings, name='admin_site_settings'),
]