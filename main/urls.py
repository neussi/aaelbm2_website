# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # À propos
    path('about/', views.about, name='about'),
    
    # Membres
    path('members/', views.members, name='members'),
    path('register/', views.member_registration, name='member_registration'),
    path('register/success/', views.member_registration_success, name='member_registration_success'),
    
    # Projets
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    
    # Événements
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/register/success/', views.event_registration_success, name='event_registration_success'),
    
    # Actualités
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Galerie
    path('gallery/', views.gallery, name='gallery'),
    
    # Dons
    path('donations/', views.donations, name='donations'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    
    # WhatsApp redirect
    path('whatsapp/', views.whatsapp_redirect, name='whatsapp_redirect'),
]

# ========================= HANDLERS D'ERREURS =========================
handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
