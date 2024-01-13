# Generated by Django 5.0 on 2024-01-13 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_home_importantlinks_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='globalAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Global Notifications',
            },
        ),
        migrations.AlterModelOptions(
            name='home_latestupdates',
            options={'verbose_name': 'update', 'verbose_name_plural': 'Updates for user'},
        ),
    ]
