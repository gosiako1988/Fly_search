from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(
        max_length=64,
        verbose_name="Nazwa kategorii")


    def __str__(self):
        return self.category_name


class FlightData(models.Model):
    fly_from = models.CharField(max_length=64)
    origin_airport_text = models.CharField(max_length=64)
    fly_to = models.CharField(max_length=64)
    destination_airport_text = models.CharField(max_length=64)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)
    return_from = models.DateField(null=True)
    return_to = models.DateField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through="FlightDataCategory")


class FlightDataCategory(models.Model):
    flight_data = models.ForeignKey(FlightData, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)