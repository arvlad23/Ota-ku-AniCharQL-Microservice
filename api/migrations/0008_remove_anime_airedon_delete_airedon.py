# Generated by Django 5.1.2 on 2024-10-30 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_airedon_incompletedata_anime_duration_anime_episodes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='airedOn',
        ),
        migrations.DeleteModel(
            name='AiredOn',
        ),
    ]