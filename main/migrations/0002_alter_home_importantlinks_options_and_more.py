# Generated by Django 5.0 on 2024-01-06 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='home_importantlinks',
            options={'verbose_name': 'link', 'verbose_name_plural': 'Important Links'},
        ),
        migrations.AlterModelOptions(
            name='home_latestupdates',
            options={'verbose_name': 'update', 'verbose_name_plural': 'Latest Updates'},
        ),
        migrations.AlterModelOptions(
            name='urltogdrive',
            options={'verbose_name': 'file', 'verbose_name_plural': 'Cloud Files'},
        ),
    ]
