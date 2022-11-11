from django.db import models


class Movie:
    def __init__(self, title, year, category, country, image, stock, price):
        self.title = title
        self.year = year
        self.category = category
        self.country = country
        self.image = image
        self.stock = stock
        self.price = price


class Domicilio(models.Model):
    calle = models.CharField(max_length=255)
    no_calle = models.IntegerField()
    pais = models.CharField(max_length=255)

    def __str__(self):
        return f'Domicilio {self.id}: {self.calle} {self.no_calle} {self.pais}'


class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    domicilio = models.ForeignKey(Domicilio, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Persona {self.id}: {self.nombre} {self.apellido} {self.email}'