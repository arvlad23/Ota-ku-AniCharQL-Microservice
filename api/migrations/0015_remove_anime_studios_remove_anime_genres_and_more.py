# Generated by Django 5.1.2 on 2024-10-30 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_genre_studio_anime_genres_anime_studios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='studios',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='genres',
        ),
        migrations.AddField(
            model_name='anime',
            name='genres',
            field=models.ManyToManyField(blank=True, default=list, null=True, related_name='genre', to='api.genre'),
        ),
    ]
