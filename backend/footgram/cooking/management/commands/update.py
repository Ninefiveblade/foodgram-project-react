import os
import json

from tqdm import tqdm
from django.core.management.base import BaseCommand

from cooking import models

data = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath("data")))
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Ingredient.objects.all().delete()
        with open(f"{data}/data/ingredients.json", "r") as j:
            data_dict = json.loads(j.read())
            count = 0
            for a in tqdm(data_dict):
                count += 1
                models.Ingredient.objects.get_or_create(
                    id=count,
                    name=a.get("name"),
                    measurement=a.get("measurement_unit")
                )
