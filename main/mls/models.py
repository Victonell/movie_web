from django.db import models

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=20, unique=True)
    poster=models.URLField()
    description=models.TextField()
    trailer_url=models.URLField()
    

    def __str__(self):
        return self.title
