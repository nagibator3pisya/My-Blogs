# Generated by Django 5.0.6 on 2024-06-27 20:30

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_article_full_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='full_description',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
