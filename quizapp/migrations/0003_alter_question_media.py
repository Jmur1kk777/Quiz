# Generated by Django 5.0.6 on 2024-08-25 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0002_remove_question_image_remove_question_video_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='question_media/'),
        ),
    ]
