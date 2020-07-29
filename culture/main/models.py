from django.db import models

class Qna(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=15)
    body = models.TextField()
    time = models.TimeField('date_published')
    phone_number = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return self.title
# Create your models here.
