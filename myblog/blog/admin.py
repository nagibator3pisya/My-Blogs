
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from blog.models import User, Article, Category, Comment, ViewCount, Like, Notification

admin.site.register(User)
# admin.site.register(Article)


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


# Автоматическое формирование slug
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


# комментарии в адм панель
@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'get_comment_content', 'created_at')

    def get_comment_content(self, obj):
        # Проверяем, есть ли связанный комментарий к статье
        if obj.article.comments.exists():
            # Возвращаем текст первого комментария к статье
            return obj.article.comments.first().content
        else:
            return "No comments"

    get_comment_content.short_description = 'Comment Content'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')