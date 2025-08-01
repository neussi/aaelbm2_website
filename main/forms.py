from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML
from .models import Member, EventRegistration, Contact

class MemberRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription des membres"""
    
    class Meta:
        model = Member
        fields = [
            'nom_prenom', 'date_naissance', 'lieu_naissance', 
            'promotion', 'telephone', 'email', 'profession', 'adresse'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Informations personnelles'),
                Row(
                    Column('nom_prenom', css_class='form-group col-md-6 mb-3'),
                    Column('promotion', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('date_naissance', css_class='form-group col-md-6 mb-3'),
                    Column('lieu_naissance', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('telephone', css_class='form-group col-md-6 mb-3'),
                    Column('email', css_class='form-group col-md-6 mb-3'),
                ),
                'profession',
                'adresse',
            ),
            HTML('''
                <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" id="terms" required>
                    <label class="form-check-label" for="terms">
                        {% trans "J'accepte les statuts et le règlement intérieur de l'association" %}
                    </label>
                </div>
            '''),
            Submit('submit', _('Envoyer ma demande d\'adhésion'), css_class='btn btn-primary btn-lg')
        )
        
        # Ajouter des classes CSS personnalisées
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class EventRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription aux événements"""
    
    class Meta:
        model = EventRegistration
        fields = ['nom_prenom', 'email', 'telephone', 'promotion', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Inscription à l\'événement'),
                Row(
                    Column('nom_prenom', css_class='form-group col-md-6 mb-3'),
                    Column('promotion', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-3'),
                    Column('telephone', css_class='form-group col-md-6 mb-3'),
                ),
                'message',
            ),
            Submit('submit', _('S\'inscrire à l\'événement'), css_class='btn btn-success btn-lg')
        )
        
        # Ajouter des classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class ContactForm(forms.ModelForm):
    """Formulaire de contact"""
    
    class Meta:
        model = Contact
        fields = ['nom_prenom', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Contactez-nous'),
                Row(
                    Column('nom_prenom', css_class='form-group col-md-6 mb-3'),
                    Column('email', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('telephone', css_class='form-group col-md-6 mb-3'),
                    Column('sujet', css_class='form-group col-md-6 mb-3'),
                ),
                'message',
            ),
            Submit('submit', _('Envoyer le message'), css_class='btn btn-primary btn-lg')
        )
        
        # Ajouter des classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class NewsletterForm(forms.Form):
    """Formulaire d'inscription à la newsletter"""
    email = forms.EmailField(
        label=_('Adresse e-mail'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Votre adresse e-mail')
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'newsletter-form'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-md-8'),
                Column(
                    Submit('submit', _('S\'abonner'), css_class='btn btn-primary'),
                    css_class='col-md-4'
                ),
            )
        )