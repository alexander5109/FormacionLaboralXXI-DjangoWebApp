from django.contrib import admin
from django.db.models import Count
from . import models

# Register your models here.

	
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'status','created_on')
	list_filter = ("status",)
	search_fields = ['title', 'content']
	prepopulated_fields = {'slug': ('title',)}
	
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'post', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)