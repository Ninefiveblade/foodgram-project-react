# Generated by Django 3.0 on 2022-07-04 20:31

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0004_auto_20220704_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='code',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=7, samples=[('Завтрак', '#ff9900'), ('Обед', '#228b22'), ('Ужин', '#9370d8')], unique=True, verbose_name='Код цвета HEX'),
        ),
    ]
