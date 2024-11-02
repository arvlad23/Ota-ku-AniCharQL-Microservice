# Generated by Django 5.1.2 on 2024-10-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_anime_score_anime_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='status',
            field=models.CharField(choices=[('Planned', 'Anons'), ('Airing', 'Ongoing'), ('Released', 'Released')], max_length=10, null=True),
        ),
    ]