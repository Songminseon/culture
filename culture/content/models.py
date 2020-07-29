from django.db import models

class Content(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    history = models.CharField(max_length=100)
    directorNm = models.CharField(max_length=20, blank=True)
  
    def __str__(self):
        name = self.name
        return name

class Content_other(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    referenceIdentifier = models.CharField(max_length=255)
    rights = models.CharField(max_length=30)
    subjectCategory = models.CharField(max_length=20)
    url = models.CharField(max_length=255)

    def __str__(self):
        title = self.title
        return self.title

    def summary(self):
        return self.description[0:30]
##영화, 연극, 뮤지컬 모두 외래키 참조해서 API로 가져올거임

# Create your models here.
