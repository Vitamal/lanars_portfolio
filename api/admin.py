from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from api.models import Image, Portfolio, Comment
from auth_users.models import User

admin.site.register(User, UserAdmin)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'portfolio')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'image')
