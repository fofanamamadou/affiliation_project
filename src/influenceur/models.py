from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.utils import timezone

class Influenceur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    code_affiliation = models.CharField(max_length=32, unique=True, editable=False)
    date_creation = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=128)  # à hasher avec set_password si login prévu

    def save(self, *args, **kwargs):
        if not self.code_affiliation:
            import uuid
            self.code_affiliation = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_affiliation_link(self):
        # Utilise le domaine du site (à configurer dans settings.py)
        base_url = getattr(settings, 'AFFILIATION_BASE_URL', 'http://localhost:8000')
        return f"{base_url}/affiliation/{self.code_affiliation}/"