from django.db import models

class Nomenclature(models.Model):
    abbreviation = models.CharField(max_length=100)
    short_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    internal_code = models.CharField(max_length=100)
    cipher = models.CharField(max_length=100)
    ekps_code = models.CharField(max_length=100)
    kvt_code = models.CharField(max_length=100)
    drawing_number = models.CharField(max_length=100)
    type_of_nomenclature = models.CharField(max_length=100)

    def __str__(self):
        return self.short_name

class LSI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
