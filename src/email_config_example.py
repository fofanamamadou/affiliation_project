#!/usr/bin/env python3
"""
Exemple de configuration email pour la production
"""

# Configuration email pour Gmail
EMAIL_CONFIG = {
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_HOST_USER': 'votre_email@gmail.com',
    'EMAIL_HOST_PASSWORD': 'votre_mot_de_passe_application',  # Mot de passe d'application Gmail
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'DEFAULT_FROM_EMAIL': 'noreply@votredomaine.com',
    'AFFILIATION_BASE_URL': 'https://votredomaine.com'
}

# Configuration email pour Outlook/Hotmail
OUTLOOK_CONFIG = {
    'EMAIL_HOST': 'smtp-mail.outlook.com',
    'EMAIL_HOST_USER': 'votre_email@outlook.com',
    'EMAIL_HOST_PASSWORD': 'votre_mot_de_passe',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'DEFAULT_FROM_EMAIL': 'noreply@votredomaine.com',
    'AFFILIATION_BASE_URL': 'https://votredomaine.com'
}

# Configuration email pour un serveur SMTP personnalisé
CUSTOM_SMTP_CONFIG = {
    'EMAIL_HOST': 'smtp.votreserveur.com',
    'EMAIL_HOST_USER': 'noreply@votredomaine.com',
    'EMAIL_HOST_PASSWORD': 'votre_mot_de_passe_smtp',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'DEFAULT_FROM_EMAIL': 'noreply@votredomaine.com',
    'AFFILIATION_BASE_URL': 'https://votredomaine.com'
}

def print_config_instructions():
    """Affiche les instructions de configuration"""
    print("📧 Configuration Email pour la Production")
    print("=" * 50)
    
    print("\n🔧 Pour configurer l'envoi d'emails en production:")
    print("1. Créez un fichier .env dans le dossier src/")
    print("2. Ajoutez les variables d'environnement suivantes:")
    print("3. Redémarrez le serveur Django")
    
    print("\n📝 Variables à ajouter dans .env:")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_HOST_USER=votre_email@gmail.com")
    print("EMAIL_HOST_PASSWORD=votre_mot_de_passe_application")
    print("EMAIL_PORT=587")
    print("EMAIL_USE_TLS=True")
    print("DEFAULT_FROM_EMAIL=noreply@votredomaine.com")
    print("AFFILIATION_BASE_URL=https://votredomaine.com")
    
    print("\n⚠️  Notes importantes:")
    print("- Pour Gmail, utilisez un mot de passe d'application (pas votre mot de passe principal)")
    print("- Activez l'authentification à 2 facteurs sur votre compte Gmail")
    print("- Générez un mot de passe d'application dans les paramètres de sécurité")
    print("- En production, mettez DEBUG=False dans les paramètres Django")
    
    print("\n🔗 Liens utiles:")
    print("- Gmail App Passwords: https://myaccount.google.com/apppasswords")
    print("- Configuration SMTP Gmail: https://support.google.com/mail/answer/7126229")

if __name__ == "__main__":
    print_config_instructions() 