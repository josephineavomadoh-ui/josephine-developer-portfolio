from django.contrib import admin
from .models import Profile, Skill, Project, Experience, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'title', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('proficiency', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('featured', 'order')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date', 'current', 'type','order')
    list_filter = ('type', 'current', 'start_date')
    search_fields = ('title', 'company', 'description')
    list_editable = ('current', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('read',)
    readonly_fields = ('created_at',)


