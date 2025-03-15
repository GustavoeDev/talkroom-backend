from django.contrib import admin
from .models import FileAttachment, AudioAttachment

@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'extension', 'size', 'content_type')

@admin.register(AudioAttachment)
class AudioAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'src')
