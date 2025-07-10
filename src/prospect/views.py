from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Prospect
from .serializers import ProspectSerializers
from influenceur.models import Influenceur
from influenceur.permissions import CanValidateProspects, IsInfluenceurOrAdmin
from influenceur.auth import get_influenceur_from_user
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@api_view(['GET', 'POST'])
@permission_classes([IsInfluenceurOrAdmin])
def prospect_view(request):
    """
    Vue API pour lister tous les prospects (GET) ou en créer un (POST).
    Seuls les influenceurs connectés et admins peuvent accéder.
    """
    if request.method == 'GET':
        # Filtrer par influenceur si ce n'est pas un admin
        current_influenceur = get_influenceur_from_user(request.user)
        if not request.user.is_superuser and current_influenceur:
            prospects = Prospect.objects.filter(influenceur=current_influenceur)
        else:
            prospects = Prospect.objects.all()
            
        serializer = ProspectSerializers(prospects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProspectSerializers(data=request.data)
        if serializer.is_valid():
            prospect = serializer.save()
            
            # Notification automatique à l'influenceur
            try:
                send_mail(
                    subject=f"Nouveau prospect via votre lien d'affiliation",
                    message=f"""
                    Bonjour {prospect.influenceur.nom},
                    
                    Un nouveau prospect s'est inscrit via votre lien d'affiliation :
                    - Nom : {prospect.nom}
                    - Email : {prospect.email}
                    - Date d'inscription : {prospect.date_inscription.strftime('%d/%m/%Y à %H:%M')}
                    
                    Votre lien d'affiliation : {prospect.influenceur.get_affiliation_link()}
                    
                    Connectez-vous à votre dashboard pour suivre vos prospects.
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[prospect.influenceur.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur lors de l'envoi de la notification : {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([CanValidateProspects])
def prospect_valider_view(request, pk):
    """
    Vue API pour valider un prospect (passer son statut à 'confirme').
    Seuls les utilisateurs avec permission de validation peuvent accéder.
    """
    prospect = get_object_or_404(Prospect, pk=pk)
    
    # Vérifier les permissions pour ce prospect spécifique
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur and prospect.influenceur != current_influenceur:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    if prospect.statut == 'confirme':
        return Response({'detail': 'Ce prospect est déjà confirmé.'}, status=status.HTTP_400_BAD_REQUEST)
    prospect.statut = 'confirme'
    prospect.save()
    serializer = ProspectSerializers(prospect)
    return Response({'detail': 'Prospect validé avec succès.', 'prospect': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsInfluenceurOrAdmin])
def prospects_sans_remise_view(request):
    """
    Vue API pour lister tous les prospects sans remise associée.
    Seuls les admins peuvent voir tous les prospects sans remise.
    """
    current_influenceur = get_influenceur_from_user(request.user)
    if not request.user.is_superuser and current_influenceur:
        prospects = Prospect.objects.filter(remise__isnull=True, influenceur=current_influenceur)
    else:
        prospects = Prospect.objects.filter(remise__isnull=True)
        
    serializer = ProspectSerializers(prospects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def affiliation_form_view(request, code_affiliation):
    """
    Vue pour afficher le formulaire d'affiliation et traiter les soumissions.
    Cette vue est publique (pas d'authentification requise).
    """
    try:
        influenceur = Influenceur.objects.get(code_affiliation=code_affiliation, is_active=True)
    except Influenceur.DoesNotExist:
        return HttpResponse('<h1>Code d\'affiliation invalide</h1>', status=404)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nom = data.get('nom')
            email = data.get('email')
            
            if not nom or not email:
                return JsonResponse({'error': 'Nom et email requis'}, status=400)
            
            # Créer le prospect
            prospect = Prospect.objects.create(
                nom=nom,
                email=email,
                influenceur=influenceur
            )
            
            # Notification automatique à l'influenceur
            try:
                send_mail(
                    subject=f"🎉 Nouveau prospect via votre lien d'affiliation !",
                    message=f"""
                    Bonjour {influenceur.nom},
                    
                    🎉 Félicitations ! Un nouveau prospect s'est inscrit via votre lien d'affiliation :
                    
                    📋 Détails du prospect :
                    - Nom : {prospect.nom}
                    - Email : {prospect.email}
                    - Date d'inscription : {prospect.date_inscription.strftime('%d/%m/%Y à %H:%M')}
                    
                    🔗 Votre lien d'affiliation : {influenceur.get_affiliation_link()}
                    
                    📊 Connectez-vous à votre dashboard pour suivre vos prospects et vos gains.
                    
                    Merci pour votre contribution !
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[influenceur.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur lors de l'envoi de la notification : {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Inscription réussie !',
                'prospect_id': prospect.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request - afficher le formulaire
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inscription via {influenceur.nom}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 500px;
                width: 100%;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .header p {{
                color: #666;
                font-size: 16px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
            }}
            input[type="text"], input[type="email"] {{
                width: 100%;
                padding: 12px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
                box-sizing: border-box;
            }}
            input[type="text"]:focus, input[type="email"]:focus {{
                outline: none;
                border-color: #667eea;
            }}
            button {{
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            button:hover {{
                transform: translateY(-2px);
            }}
            .success {{
                display: none;
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
            }}
            .error {{
                display: none;
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Inscription via {influenceur.nom}</h1>
                <p>Remplissez le formulaire ci-dessous pour vous inscrire</p>
            </div>
            
            <form id="affiliationForm">
                <div class="form-group">
                    <label for="nom">Nom complet *</label>
                    <input type="text" id="nom" name="nom" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email *</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <button type="submit">S'inscrire</button>
            </form>
            
            <div id="success" class="success">
                ✅ Inscription réussie ! Merci de vous être inscrit via {influenceur.nom}.
            </div>
            
            <div id="error" class="error">
                ❌ Une erreur s'est produite. Veuillez réessayer.
            </div>
        </div>
        
        <script>
            document.getElementById('affiliationForm').addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                const formData = {{
                    nom: document.getElementById('nom').value,
                    email: document.getElementById('email').value
                }};
                
                try {{
                    const response = await fetch(window.location.href, {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify(formData)
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        document.getElementById('success').style.display = 'block';
                        document.getElementById('error').style.display = 'none';
                        document.getElementById('affiliationForm').style.display = 'none';
                    }} else {{
                        document.getElementById('error').textContent = result.error || 'Une erreur s\'est produite';
                        document.getElementById('error').style.display = 'block';
                        document.getElementById('success').style.display = 'none';
                    }}
                }} catch (error) {{
                    document.getElementById('error').textContent = 'Erreur de connexion';
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('success').style.display = 'none';
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(html_content, content_type='text/html')