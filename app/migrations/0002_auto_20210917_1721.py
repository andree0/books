# Generated by Django 3.2.7 on 2021-09-17 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='lang',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='book',
            name='link',
            field=models.URLField(),
        ),
    ]