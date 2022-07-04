# Generated by Django 3.0 on 2022-07-04 20:16

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название ингридиента', max_length=128, verbose_name='Название ингредиента')),
                ('measurement', models.CharField(help_text='Введите единицу измерения', max_length=15, verbose_name='Единица измерения ингридиента')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(help_text='Введите количество ингридиента', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество ингридиента')),
            ],
            options={
                'verbose_name': 'Количество ингридиента',
                'verbose_name_plural': 'Количество ингридиентов',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название рецепта', max_length=128, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка блюда')),
                ('description', models.TextField(help_text='Введите описание рецепта', verbose_name='Описание рецепта')),
                ('time', models.IntegerField(help_text='Введите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в минутах')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите имя тега', max_length=128, unique=True, verbose_name='Имя тега')),
                ('code', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=7, samples=None, unique=True, verbose_name='Код цвета HEX')),
                ('slug', models.SlugField(help_text='Введите slug поле Тега', max_length=128, unique=True, verbose_name='slug поле Тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Тэги',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='ShopList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ManyToManyField(related_name='shop_recipe', to='cooking.Recipe', verbose_name='Избранный рецепт')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'ordering': ['id'],
            },
        ),
    ]
