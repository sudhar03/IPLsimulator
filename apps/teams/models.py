from django.db import models
from model_utils import Choices



class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="logo", blank=True, null=True)
    year = models.IntegerField()
    
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"{self.name} - {self.year}"

class GenericPlayer(models.Model):
    NATIONALITY = Choices("INDIAN", "OVERSEAS",)
    name = models.CharField(max_length=255)
    player_type = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255, choices=NATIONALITY, null=True, blank=True)
    base_price = models.IntegerField()

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return f"{self.name} - {self.player_type} - {self.nationality}"


import csv

def import_players_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader.fieldnames)
        count = 0
        for row in reader:
            try:
                # Clean and convert nationality
                raw_nationality = row['nationality'].strip().lower()
                nationality_value = GenericPlayer.NATIONALITY.INDIAN if raw_nationality == 'india' else GenericPlayer.NATIONALITY.OVERSEAS

                # Convert base price from lakhs to paise
                base_price_lakhs_raw = row['base price (in lacs)'].strip()
                if base_price_lakhs_raw and base_price_lakhs_raw.replace('.', '').isdigit():
                    base_price_lakhs = float(base_price_lakhs_raw)
                else:
                    base_price_lakhs = 50  # Default to 50 lakhs

                base_price_paise = int(base_price_lakhs * 100000 * 100) # 1 lakh = 100000 rupees, 1 rupee = 100 paise

                GenericPlayer.objects.create(
                    name=row['name'].strip(),
                    player_type=row['player style'].strip(),
                    nationality=nationality_value,
                    base_price=base_price_paise  # Assuming base_price is an IntegerField storing paise
                )
                count += 1
            except Exception as e:
                print(f"❌ Error importing row {row}: {e}")
        print(f"✅ Successfully imported {count} players.")