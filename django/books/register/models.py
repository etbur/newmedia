from django.db import models

# Create your models here.
class book(models.Model):
  name=models.CharField(max_length=50)
  author=models.CharField(max_length=50)
  title=models.CharField(max_length=50)
  publish_date=models.DateField()
  def __str__(self) :
    return self.title
