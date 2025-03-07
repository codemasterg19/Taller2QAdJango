from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    height = models.FloatField()
    image = models.URLField()  # Asegúrate de que la imagen sea una URL válida

    def __str__(self):
        return self.name
