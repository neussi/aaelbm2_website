# 🎓 A²ELBM2 - Site Web de l'Association

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-v5.3-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Site web officiel de l'**Association des Anciens Élèves du Lycée Bilingue de Monatélé 2** (A²ELBM2) avec un dashboard administrateur complet.

## 🌟 Fonctionnalités

### 📱 Site Public
- **Page d'accueil** moderne et responsive
- **Présentation de l'association** avec historique
- **Liste des membres** avec filtres
- **Projets** avec suivi financier en temps réel
- **Événements** avec système d'inscription
- **Actualités** multilingues (FR/EN)
- **Galerie multimédia** (photos/vidéos)
- **Formulaire de contact** avec notifications
- **Support multilingue** français/anglais

### 🔐 Dashboard Administrateur
- **Authentification sécurisée** avec gestion des permissions
- **Tableau de bord** avec statistiques en temps réel
- **Gestion complète des membres** (CRUD + approbation)
- **Gestion des projets** avec timeline et budget
- **Gestion des événements** et inscriptions
- **Publication d'actualités** avec éditeur riche
- **Galerie multimédia** avec upload d'images/vidéos
- **Messages de contact** avec réponses WhatsApp/Email
- **Paramètres du site** centralisés

## 🚀 Installation

### Prérequis
```bash
Python 3.8+
Django 4.2+
pip (gestionnaire de paquets Python)
```

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/a2elbm2-website.git
cd a2elbm2-website
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 6. Collecter les fichiers statiques
```bash
python manage.py collectstatic
```

### 7. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le site sera accessible à : `http://127.0.0.1:8000/`
Dashboard admin : `http://127.0.0.1:8000/admin/`

## 📦 Dépendances

```txt
Django==4.2.7
django-ckeditor==6.7.0
django-modeltranslation==0.18.11
django-crispy-forms==2.0
crispy-bootstrap5==0.7
Pillow==10.0.1
python-decouple==3.8
```

## 🏗️ Structure du Projet

```
aaelbm2_website/
├── 📁 main/                          # Application principale
│   ├── 📁 models/                    # Modèles de données
│   ├── 📁 views/                     # Vues du site public
│   ├── 📁 templates/                 # Templates du site public
│   └── 📁 static/                    # Fichiers statiques
├── 📁 admin_dashboard/               # Dashboard administrateur
│   ├── 📁 templates/admin_dashboard/ # Templates admin
│   │   ├── 📁 auth/                  # Authentification
│   │   ├── 📁 members/               # Gestion membres
│   │   ├── 📁 projects/              # Gestion projets
│   │   ├── 📁 events/                # Gestion événements
│   │   ├── 📁 news/                  # Gestion actualités
│   │   ├── 📁 gallery/               # Gestion galerie
│   │   ├── 📁 messages/              # Gestion messages
│   │   └── 📁 settings/              # Paramètres
│   ├── views.py                      # Vues admin
│   ├── auth_views.py                 # Authentification
│   ├── forms.py                      # Formulaires
│   ├── urls.py                       # URLs admin
│   └── middleware.py                 # Middleware sécurité
├── 📁 templates/                     # Templates globaux
├── 📁 static/                        # Fichiers statiques globaux
├── 📁 media/                         # Fichiers uploadés
├── 📁 locale/                        # Fichiers de traduction
├── 📁 logs/                          # Logs de l'application
├── manage.py                         # Script de gestion Django
├── requirements.txt                  # Dépendances Python
└── README.md                         # Documentation
```

## 🔧 Configuration

### Variables d'Environnement
Créez un fichier `.env` à la racine du projet :

```env
# Configuration de base
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données (optionnel, SQLite par défaut)
DATABASE_URL=postgres://user:password@localhost:5432/a2elbm2_db

# Configuration email
EMAIL_HOST_USER=propentatech@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=A²ELBM2 <propentatech@gmail.com>

# Contacts WhatsApp
WHATSAPP_PRESIDENT=+237673583241
WHATSAPP_TREASURER_MTN=683533430
WHATSAPP_TREASURER_ORANGE=698810079
```

### Configuration Email
Pour activer l'envoi d'emails :
1. Activez l'authentification à 2 facteurs sur Gmail
2. Générez un mot de passe d'application
3. Mettez à jour `EMAIL_HOST_PASSWORD` dans les settings

## 🎨 Personnalisation

### Couleurs et Design
Modifiez les variables CSS dans `static/css/style.css` :

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --text-dark: #2d3748;
    --text-light: #718096;
}
```

### Logo et Images
- **Logo** : Remplacez `static/images/logo.png`
- **Image d'accueil** : Remplacez `static/images/hero-bg.jpg`
- **Favicon** : Remplacez `static/images/favicon.ico`

## 👥 Gestion des Utilisateurs

### Rôles et Permissions
- **Superuser** : Accès complet au Django admin et dashboard
- **Staff** : Accès au dashboard admin uniquement
- **Membre** : Accès au site public uniquement

### Créer un Administrateur
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='admin_nom',
    email='admin@a2elbm2.org',
    password='mot_de_passe_securise',
    first_name='Prénom',
    last_name='Nom'
)
user.is_staff = True
user.save()
```

## 📧 Configuration des Notifications

### WhatsApp
Les liens WhatsApp sont générés automatiquement :
```python
# Format : https://wa.me/NUMERO?text=MESSAGE
# Exemple : https://wa.me/237673583241?text=Bonjour...
```

### Emails Automatiques
- **Nouvelle demande d'adhésion** → Notifications admin
- **Inscription événement** → Confirmation membre
- **Nouveau message contact** → Notification admin
- **Demande accès admin** → Notification superusers

## 🛡️ Sécurité

### Mesures Implémentées
- ✅ **Protection CSRF** sur tous les formulaires
- ✅ **Authentification obligatoire** pour l'admin
- ✅ **Validation des permissions** (staff_member_required)
- ✅ **Sessions sécurisées** avec timeout
- ✅ **Validation des uploads** (type, taille)
- ✅ **Middleware de protection** personnalisé

### Recommandations Production
```python
# Dans settings.py pour la production
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

## 🚀 Déploiement

### Avec Heroku
```bash
# Installer Heroku CLI
heroku create a2elbm2-website
heroku config:set SECRET_KEY=votre-clé-secrète
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Avec VPS (Ubuntu)
```bash
# Installer dépendances
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# Configurer PostgreSQL
sudo -u postgres createdb a2elbm2_db
sudo -u postgres createuser a2elbm2_user

# Configurer Nginx
sudo nano /etc/nginx/sites-available/a2elbm2

# Configurer Gunicorn
pip install gunicorn
gunicorn aaelbm2_website.wsgi:application
```

## 📊 Fonctionnalités Techniques

### Performance
- **Cache** : Mise en cache des statistiques (5 min)
- **Pagination** : Optimisée pour grandes listes
- **Lazy Loading** : Chargement paresseux des images
- **Compression** : Fichiers CSS/JS minifiés

### SEO
- **URLs SEO-friendly** avec slugs
- **Meta tags** dynamiques
- **Sitemap** XML généré automatiquement
- **Support multilingue** avec hreflang

### Analytics
- **Logs détaillés** dans `/logs/admin.log`
- **Statistiques d'usage** dans le dashboard
- **Suivi des actions** admin avec timestamps

## 🐛 Résolution de Problèmes

### Erreurs Communes

**1. Erreur de migration**
```bash
python manage.py makemigrations --empty main
python manage.py migrate --fake-initial
```

**2. Problème d'upload de fichiers**
```bash
chmod 755 media/
```

**3. Erreur CSS/JS non chargés**
```bash
python manage.py collectstatic --clear
```

**4. Problème d'email**
```python
# Tester la configuration email
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Message test', 'from@example.com', ['to@example.com'])
```

## 📞 Support et Contact

### Équipe de Développement
- **Développeur Principal** : [Votre Nom]
- **Email** : propentatech@gmail.com
- **WhatsApp** : +237673583241

### Association A²ELBM2
- **Site Web** : https://a2elbm2.org
- **Email** : propentatech@gmail.com
- **Adresse** : Yaoundé, Cameroun

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créez une **branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Commitez** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Guidelines de Contribution
- Suivez les conventions de code Python (PEP 8)
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Utilisez des messages de commit descriptifs

## 📈 Roadmap

### Version 2.0 (À venir)
- [ ] **API REST** pour mobile app
- [ ] **Système de notifications** push
- [ ] **Chat en temps réel** entre membres
- [ ] **Module de parrainage** pour nouveaux membres
- [ ] **Système de vote** électronique
- [ ] **Intégration mobile money** pour cotisations
- [ ] **Module d'emploi** pour anciens élèves

### Version 1.1 (Améliorations)
- [ ] **Export Excel** des listes
- [ ] **Calendrier** intégré pour événements
- [ ] **Module de newsletters**
- [ ] **Système de badges** pour membres actifs
- [ ] **Intégration réseaux sociaux** poussée

## 🎯 Fonctionnalités Avancées

### Dashboard Analytics
- Statistiques de visites en temps réel
- Graphiques d'évolution des membres
- Suivi des projets avec KPI
- Rapport d'activité mensuel automatique

### Automatisation
- Emails de rappel pour événements
- Notifications d'anniversaire des membres
- Sauvegarde automatique de la base de données
- Génération de rapports périodiques

---

<div align="center">

**Développé avec ❤️ pour l'Association A²ELBM2**

*Gardez le lien, cultivez l'excellence !*

</div>