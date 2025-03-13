from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.URLField()
    height = models.FloatField()
    weight = models.FloatField()
    base_experience = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    abilities = models.JSONField(default=list, blank=True, null=True)
    types = models.JSONField(default=list, blank=True, null=True)
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)

    def __str__(self):
        return self.name
