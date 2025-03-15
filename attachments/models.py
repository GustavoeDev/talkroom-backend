from django.db import models


class FileAttachment(models.Model):
    name = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    size = models.FloatField()
    src = models.TextField()
    content_type = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'file_attachments'

    def __str__(self):
        return self.name
    

class AudioAttachment(models.Model):
    src = models.TextField()

    class Meta:
        db_table = 'audio_attachments'