from django.db import models
from django.db.models import URLField


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING, max_length=30
    )
    last_update = models.DateTimeField(auto_now=True, editable=True)
    application_link = URLField(blank=True)
    notes = models.TextField(blank=True, max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"
