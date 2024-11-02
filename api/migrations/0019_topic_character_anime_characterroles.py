# Generated by Django 5.1.2 on 2024-10-30 22:25

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_externallink_alter_anime_genres_alter_anime_studios_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('commentsCount', models.IntegerField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(blank=True, null=True)),
                ('updatedAt', models.DateTimeField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('htmlBody', models.TextField(blank=True, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('type', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('descriptionHtml', models.TextField(blank=True, null=True)),
                ('descriptionSource', models.TextField(blank=True, null=True)),
                ('isAnime', models.BooleanField(default=False)),
                ('isManga', models.BooleanField(default=False)),
                ('isRanobe', models.BooleanField(default=False)),
                ('japanese', models.TextField(blank=True, null=True)),
                ('malId', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=120)),
                ('russian', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.poster')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.topic')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='characterRoles',
            field=models.ManyToManyField(blank=True, default=dict, to='api.character'),
        ),
    ]