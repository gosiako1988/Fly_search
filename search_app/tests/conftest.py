import pytest
from django.contrib.auth.models import User
from django.test import Client

from search_app.models import FlightData, Category


@pytest.fixture
def client():
    user = User.objects.create(
        username="test1",
        password="test1",
        first_name="test1",
        last_name="test1",
        email="test1@test.pl",
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def flight_data():
    fly = FlightData.objects.create(
        fly_from="WAW",
        origin_airport_text="Lotnisko Chopina w Warszawie",
        fly_to="MPX",
        destination_airport_text="Port lotniczy Mediolan-Malpensa",
        adults=1,
        children=0,
        infants=0,
        date_from="2023-12-16",
        date_to="2024-01-16",
        return_from="2023-12-16",
        return_to="2024-01-16",
        price=3000,
        user=user,
    )

    return fly

@pytest.fixture
def new_category():
    new_category = Category.objects.create(category_name="wakacje")

    return new_category