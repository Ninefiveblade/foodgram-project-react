"""Command module for Foodgram project database."""
import json
import os

from cooking import models
from django.core.management.base import BaseCommand
from tqdm import tqdm

data = os.path.abspath("../data")


class Command(BaseCommand):
    """Comand for deploy data to database."""

    def handle(self, *args, **options):
        models.Ingredient.objects.all().delete()
        with open(f"{data}/ingredients.json", "r") as j:
            data_dict = json.loads(j.read())
            count = 0
            try:
                for a in tqdm(data_dict):
                    count += 1
                    models.Ingredient.objects.get_or_create(
                        id=count,
                        name=a.get("name"),
                        measurement=a.get("measurement_unit")
                    )
                print("Загрузка ингридиентов завершена! "
                      f"Загружено товаров: {len(data_dict)}")
            except Exception as er:
                print("Что-то не так с моделями, путями или базой данных "
                      f"проверьте, ошибка: {er}")
