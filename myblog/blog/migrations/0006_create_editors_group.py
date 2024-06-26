# Generated by Django 5.0.6 on 2024-06-23 10:39

from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Создаем группу "Редакторы"
    editors_group, created = Group.objects.get_or_create(name='Редакторы')

    # Назначаем разрешения
    permissions = Permission.objects.filter(content_type__app_label='blog', codename__in=[
        'change_article',
        'delete_article'
    ])
    editors_group.permissions.set(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_viewcount'),  # Убедитесь, что здесь указана последняя миграция
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]