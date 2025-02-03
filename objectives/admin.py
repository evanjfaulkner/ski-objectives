from django.contrib import admin
from .models import SkiObjective, InterestedParty

@admin.register(SkiObjective)
class SkiObjectiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'distance', 'vertical_gain', 'interest_level', 'best_season')
    list_filter = ('interest_level', 'best_season', 'area', 'type')
    search_fields = ('name', 'area', 'notes')

@admin.register(InterestedParty)
class InterestedPartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'objective', 'email', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('name', 'email', 'objective__name') 