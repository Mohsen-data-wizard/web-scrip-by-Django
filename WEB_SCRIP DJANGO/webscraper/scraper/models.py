from django.db import models

class Product(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()

    def __str__(self):
        return self.name
