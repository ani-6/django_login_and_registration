# Generated by Django 5.0.6 on 2024-11-15 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='cover_pic',
            new_name='cover_picture',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='remote_fol_id',
            new_name='remote_folder_id',
        ),
    ]
