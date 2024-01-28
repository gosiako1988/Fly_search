from django.contrib import admin

# Register your models here.
from search_app.models import (Category, FlightData)
admin.site.register(Category)
admin.site.register(FlightData)