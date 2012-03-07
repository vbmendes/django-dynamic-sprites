from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    flag = models.ImageField(upload_to='img/country/flags')
