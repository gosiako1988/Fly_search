import pytest

from search_app.models import FlightData, Category

@pytest.mark.django_db
def test_details(client):
    response = client.get('')
    assert response.status_code == 200

@pytest.mark.django_db
def test_login(client):
    response = client.post("/login/", {'username': 'test1', 'password': 'test1@test.pl'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_fly(client, new_category):
    response = client.post("/search/?origin_airport_text=Lotnisko+Chopina+w+Warszawie&origin_airport=WAW&destination_airport_text=Port+lotniczy+Mediolan-Malpensa&destination_airport=MXP&adults=1&children=0&infants=0&date_from=2023-12-16&date_to=2024-01-16&return_from=2023-12-16&return_to=2024-01-16", data={"price": '1000', "categories": "wakacje"})
    assert response.status_code == 200
    assert FlightData.objects.count() > 0