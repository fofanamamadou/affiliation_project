#!/usr/bin/env python3
"""
Script pour récupérer la SECRET_KEY actuelle du projet
"""

import os
import sys

def get_current_secret_key():
    """Récupère la SECRET_KEY actuelle du projet"""
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    
    try:
        import django
        django.setup()
        
        from django.conf import settings
        
        print("🔑 Récupération de la SECRET_KEY actuelle")
        print("=" * 50)
        
        current_secret_key = settings.SECRET_KEY
        
        print(f"✅ SECRET_KEY actuelle trouvée :")
        print(f"SECRET_KEY={current_secret_key}")
        
        print(f"\n📝 Copiez cette ligne dans votre fichier .env :")
        print(f"SECRET_KEY={current_secret_key}")
        
        print(f"\n⚠️  IMPORTANT :")
        print(f"- Cette clé est actuellement utilisée par votre projet")
        print(f"- Si vous changez cette clé, tous les utilisateurs seront déconnectés")
        print(f"- Les sessions existantes seront invalidées")
        print(f"- Les tokens JWT existants deviendront invalides")
        
        return current_secret_key
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération : {str(e)}")
        return None

def check_secret_key_security():
    """Vérifie la sécurité de la SECRET_KEY"""
    
    try:
        import django
        django.setup()
        
        from django.conf import settings
        
        secret_key = settings.SECRET_KEY
        
        print(f"\n🔒 Analyse de sécurité de la SECRET_KEY :")
        print(f"- Longueur : {len(secret_key)} caractères")
        
        if len(secret_key) < 50:
            print(f"⚠️  ATTENTION : Clé trop courte ! Recommandé : 50+ caractères")
        else:
            print(f"✅ Longueur acceptable")
        
        # Vérifier la complexité
        has_letters = any(c.isalpha() for c in secret_key)
        has_digits = any(c.isdigit() for c in secret_key)
        has_special = any(c in '!@#$%^&*(-_=+)' for c in secret_key)
        
        print(f"- Contient des lettres : {'✅' if has_letters else '❌'}")
        print(f"- Contient des chiffres : {'✅' if has_digits else '❌'}")
        print(f"- Contient des caractères spéciaux : {'✅' if has_special else '❌'}")
        
        if has_letters and has_digits and has_special:
            print(f"✅ Complexité acceptable")
        else:
            print(f"⚠️  Recommandé : mélanger lettres, chiffres et caractères spéciaux")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {str(e)}")

if __name__ == "__main__":
    current_key = get_current_secret_key()
    
    if current_key:
        check_secret_key_security()
        
        print(f"\n💡 Recommandations :")
        print(f"1. Utilisez cette clé dans votre fichier .env")
        print(f"2. En production, générez une nouvelle clé")
        print(f"3. Changez la clé régulièrement pour la sécurité")
        print(f"4. Ne partagez jamais cette clé") 