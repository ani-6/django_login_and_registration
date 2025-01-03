# Generated by Django 5.0.6 on 2024-11-15 13:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_globalannouncement_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Home_LatestUpdates',
            new_name='LatestUpdates',
        ),
        migrations.RenameField(
            model_name='globalannouncement',
            old_name='body',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='image_gallery',
            old_name='thumb',
            new_name='thumbnail',
        ),
        migrations.RenameField(
            model_name='urltogdrive',
            old_name='fileid',
            new_name='file_id',
        ),
        migrations.RenameField(
            model_name='urltogdrive',
            old_name='shared',
            new_name='is_shared',
        ),
        migrations.RemoveField(
            model_name='urltogdrive',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='urltogdrive',
            name='folderid',
        ),
        migrations.RemoveField(
            model_name='urltogdrive',
            name='original_path',
        ),
        migrations.AddField(
            model_name='urltogdrive',
            name='file_name',
            field=models.CharField(default='test', max_length=255, verbose_name='File name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urltogdrive',
            name='folder_id',
            field=models.CharField(default='test', max_length=255, verbose_name='Drive folder Id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urltogdrive',
            name='source_path',
            field=models.CharField(default='test', max_length=255, verbose_name='Source path'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ImportantLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255, verbose_name='Heading')),
                ('description', models.CharField(max_length=1024, verbose_name='Description')),
                ('link', models.CharField(help_text="Enter the full internal url without '/' e.g. 'explore/'", max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'Important links',
            },
        ),
        migrations.DeleteModel(
            name='Home_ImportantLinks',
        ),
    ]
