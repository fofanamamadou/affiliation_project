from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """
    Service d'envoi d'emails pour le système d'affiliation
    """
    
    @staticmethod
    def send_affiliation_link(influenceur):
        """
        Envoie un email avec le lien d'affiliation à un influenceur
        """
        try:
            subject = f"Votre lien d'affiliation - {influenceur.nom}"
            
            # Contexte pour le template
            context = {
                'influenceur': influenceur,
                'affiliation_link': influenceur.get_affiliation_link(),
                'base_url': getattr(settings, 'AFFILIATION_BASE_URL', 'http://localhost:8000'),
                'site_name': 'Système d\'Affiliation'
            }
            
            # Rendu du template HTML
            html_message = render_to_string('influenceur/email_affiliation_link.html', context)
            
            # Version texte simple
            text_message = f"""
Bonjour {influenceur.nom},

Votre compte d'influenceur a été créé avec succès !

Votre lien d'affiliation : {influenceur.get_affiliation_link()}

Vous pouvez utiliser ce lien pour promouvoir nos produits et gagner des commissions.

Cordialement,
L'équipe {context['site_name']}
            """.strip()
            
            # Envoi de l'email
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[influenceur.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email d'affiliation envoyé avec succès à {influenceur.email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email d'affiliation à {influenceur.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(influenceur):
        """
        Envoie un email de bienvenue à un nouvel influenceur
        """
        try:
            subject = f"Bienvenue dans notre programme d'affiliation - {influenceur.nom}"
            
            context = {
                'influenceur': influenceur,
                'affiliation_link': influenceur.get_affiliation_link(),
                'base_url': getattr(settings, 'AFFILIATION_BASE_URL', 'http://localhost:8000'),
                'site_name': 'Système d\'Affiliation'
            }
            
            html_message = render_to_string('influenceur/email_welcome.html', context)
            
            text_message = f"""
Bienvenue {influenceur.nom} !

Nous sommes ravis de vous accueillir dans notre programme d'affiliation.

Votre lien d'affiliation : {influenceur.get_affiliation_link()}

Commencez dès maintenant à promouvoir nos produits et à gagner des commissions !

Cordialement,
L'équipe {context['site_name']}
            """.strip()
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[influenceur.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email de bienvenue envoyé avec succès à {influenceur.email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de bienvenue à {influenceur.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_commission_notification(influenceur, prospect, commission_amount):
        """
        Envoie une notification de commission à un influenceur
        """
        try:
            subject = f"Nouvelle commission gagnée - {influenceur.nom}"
            
            context = {
                'influenceur': influenceur,
                'prospect': prospect,
                'commission_amount': commission_amount,
                'site_name': 'Système d\'Affiliation'
            }
            
            html_message = render_to_string('influenceur/email_commission.html', context)
            
            text_message = f"""
Félicitations {influenceur.nom} !

Vous avez gagné une nouvelle commission de {commission_amount} F CFA grâce au prospect {prospect.nom}.

Continuez comme ça !

Cordialement,
L'équipe {context['site_name']}
            """.strip()
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[influenceur.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Notification de commission envoyée à {influenceur.email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la notification de commission à {influenceur.email}: {str(e)}")
            return False 