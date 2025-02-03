from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class SkiObjective(models.Model):
    DIFFICULTY_CHOICES = [
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
        ('4', 'Expert'),
        ('5', 'Extreme'),
    ]

    INTEREST_CHOICES = [
        ('BURNING', 'Burning'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('MILD', 'Mild'),
    ]

    name = models.CharField(max_length=200)
    distance = models.FloatField(help_text="Distance in miles", null=True, blank=True)
    vertical_gain = models.IntegerField(help_text="Vertical gain in feet", null=True, blank=True)
    area = models.CharField(max_length=200, null=True, blank=True)
    aspect = models.CharField(max_length=100, null=True, blank=True)
    trip_report_link = models.URLField(null=True, blank=True)
    interest_level = models.CharField(max_length=20, choices=INTEREST_CHOICES, null=True, blank=True)
    done_before = models.BooleanField(default=False)
    type = models.CharField(max_length=100, null=True, blank=True)
    skill_level = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    strenuous_level = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    lowest_elevation = models.IntegerField(null=True, blank=True)
    highest_elevation = models.IntegerField(null=True, blank=True)
    best_season = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(blank=True)
    interested_people = models.TextField(blank=True)
    
    # Keep the existing fields for future use
    gpx_file = models.FileField(upload_to='gpx_files/', null=True, blank=True)
    strava_embed_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('objective-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-interest_level', 'name']

class InterestedParty(models.Model):
    objective = models.ForeignKey(SkiObjective, on_delete=models.CASCADE, related_name='interested_parties')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Interested Parties"

    def __str__(self):
        return f"{self.name} - {self.objective.name}" 