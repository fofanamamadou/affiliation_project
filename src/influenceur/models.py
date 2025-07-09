from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Influenceur(models.Model):
    nom = models.CharField(max_length=100)
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