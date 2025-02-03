import csv
from django.core.management.base import BaseCommand
from objectives.models import SkiObjective

class Command(BaseCommand):
    help = 'Import ski objectives from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['Objective']:  # Skip empty rows
                    continue
                    
                # Convert interest level to choice format
                interest_level = row['Interest Level'].upper() if row['Interest Level'] else None
                
                # Create or update the objective
                objective, created = SkiObjective.objects.update_or_create(
                    name=row['Objective'],
                    defaults={
                        'distance': float(row['Distance [mi]']) if row['Distance [mi]'] else None,
                        'vertical_gain': int(row['Vert [ft]']) if row['Vert [ft]'] else None,
                        'area': row['Area'],
                        'aspect': row['Aspect'],
                        'trip_report_link': row['Map/ Trip Report'],
                        'interest_level': interest_level,
                        'done_before': row['Done before?'].upper() == 'TRUE',
                        'type': row['Type'],
                        'skill_level': row['Skill'] if row['Skill'] else None,
                        'strenuous_level': row['Strenuous'] if row['Strenuous'] else None,
                        'lowest_elevation': int(row['Lowest elevation']) if row['Lowest elevation'] else None,
                        'highest_elevation': int(row['Highest elevation']) if row['Highest elevation'] else None,
                        'best_season': row['Best Time of Year'],
                        'notes': row['Notes'],
                        'interested_people': row['Interested People'],
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created objective "{row["Objective"]}"'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated objective "{row["Objective"]}"')) 