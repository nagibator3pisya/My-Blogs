# Generated by Django 5.0.6 on 2024-06-12 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_article_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='About_me',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='Programming_skills',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
