# Generated by Django 5.0.6 on 2024-08-25 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='video',
        ),
        migrations.AddField(
            model_name='question',
            name='media',
            field=models.ImageField(blank=True, null=True, upload_to='question_media/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='time_limit',
            field=models.IntegerField(choices=[(5, '5 seconds'), (10, '10 seconds'), (20, '20 seconds'), (30, '30 seconds'), (45, '45 seconds'), (60, '1 minute'), (90, '1 minute 30 seconds'), (120, '2 minutes'), (180, '3 minutes')], default=30),
        ),
    ]
