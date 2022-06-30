# Generated by Django 2.2.16 on 2022-06-30 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название ингридиента', max_length=128, verbose_name='Название ингредиента')),
                ('quantity', models.IntegerField(help_text='Введите количество ингридиента', null=True, verbose_name='Количество ингридиента')),
                ('measurement', models.CharField(help_text='Введите единицу измерения', max_length=15, verbose_name='Единица измерения ингридиента')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Введите название рецепта', max_length=128, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка блюда')),
                ('description', models.TextField(help_text='Введите описание рецепта', verbose_name='Описание рецепта')),
                ('time', models.TimeField(help_text='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('ingredient', models.ManyToManyField(help_text='Выберите ингридиенты рецепта', related_name='reciepe_ingredient', to='cooking.Ingredient', verbose_name='Ингридиенты рецепта')),
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
                ('code', models.CharField(help_text='Введите код цвета HEX', max_length=128, unique=True, verbose_name='Код цвета HEX')),
                ('slug', models.SlugField(help_text='Введите slug поле Тега', max_length=128, unique=True, verbose_name='slug поле Тега')),
                ('recipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipe_tag', to='cooking.Recipe')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Тэги',
                'ordering': ['-name'],
            },
        ),
    ]