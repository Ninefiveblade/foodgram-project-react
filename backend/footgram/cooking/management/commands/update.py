import csv
import os
import json

from tqdm import tqdm
from django.core.management.base import BaseCommand

from cooking import models

data = os.path.abspath("data")

class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Ingredient.objects.all().delete()
        with open(f"{data}/ingredients.csv", "r") as table:
            reader = csv.DictReader(table)
        with open(f"{data}/ingredients.json", "r") as j:
            data_dict = json.loads(j.read())
            for a in tqdm(data_dict):
                models.Ingredient.objects.get_or_create(
                    name=a.get("name"),
                    measurement=a.get("measurement_unit")
                )
"""
@todo Сделать добавление по csv файлу в том числе.
"""