#!/usr/bin/env python3
"""
Script pour générer une nouvelle SECRET_KEY Django
"""

import secrets
import string

def generate_secret_key():
    """Génère une nouvelle SECRET_KEY Django"""
    
    # Caractères autorisés pour Django SECRET_KEY
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Générer une clé de 50 caractères
    secret_key = ''.join(secrets.choice(chars) for _ in range(50))
    
    return secret_key

def main():
    """Fonction principale"""
    print("🔑 Générateur de SECRET_KEY Django")
    print("=" * 40)
    
    # Générer la clé
    secret_key = generate_secret_key()
    
    print(f"\n✅ Votre nouvelle SECRET_KEY :")
    print(f"SECRET_KEY='{secret_key}'")
    
    print(f"\n📝 Copiez cette ligne dans votre fichier .env :")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n⚠️  IMPORTANT :")
    print(f"- Gardez cette clé secrète")
    print(f"- Ne la partagez jamais")
    print(f"- Utilisez une clé différente pour chaque environnement")
    print(f"- En production, changez cette clé régulièrement")
    
    print(f"\n🔒 Cette clé est utilisée pour :")
    print(f"- Signer les sessions utilisateur")
    print(f"- Crypter les tokens JWT")
    print(f"- Sécuriser les formulaires CSRF")
    print(f"- Hasher les mots de passe")
    
    return secret_key

if __name__ == "__main__":
    main() 