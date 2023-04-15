from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score')
    list_filter = ('score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
