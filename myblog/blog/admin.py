from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin

from blog.models import User, Article, Category

admin.site.register(User)
admin.site.register(Article)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )

