# Generated by Django 2.2.1 on 2019-05-22 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_auto_20190522_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_quantity',
                                    to='app.Recipe'),
        ),
    ]
