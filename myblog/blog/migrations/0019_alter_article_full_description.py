# Generated by Django 5.0.6 on 2024-06-28 21:37

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_article_full_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='full_description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Полное описание'),
        ),
    ]
