import smtplib

from django.core.management.base import BaseCommand, CommandError
from search_app.models import FlightData
import requests

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2"
TEQUILA_API_KEY = "Q_vLi3x_VS-0ze9glMSWHCWOmr7VxZB3"
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = "malgosianow1988@gmail.com"
# MY_PASSWORD = "Alanek120908@"
# TEST_MAIL = "paskowy1990@gmail.com"
MY_PASSWORD = "ryen cyzr mzln uyxk"


class Command(BaseCommand):
    """Automatic API query for saved flights and sending miles to the user if the price of the saved flight drops"""


    def handle(self, *args, **options):
        location_endpoint = f"{TEQUILA_ENDPOINT}/search"
        headers = {"apikey": TEQUILA_API_KEY}
        try:
            flights = FlightData.objects.all()


            for flight in flights:

                date_from = flight.date_from.strftime('%d/%m/%Y')
                date_to = flight.date_to.strftime('%d/%m/%Y')
                return_from = flight.return_from.strftime('%d/%m/%Y')
                return_to = flight.return_to.strftime('%d/%m/%Y')

                query = {
                    "fly_from": flight.fly_from,
                    "fly_to": flight.fly_to,
                    "adults": flight.adults,
                    "children": flight.children,
                    "infants": flight.infants,
                    "max_stopovers": 0,
                    "date_from": date_from,
                    "date_to": date_to,
                    "return_from": return_from,
                    "return_to": return_to,
                    "curr": "PLN",
                    "sort": "price",
                    "locale": "pl",
                    "limit": 10
                }

                response = requests.get(url=location_endpoint, headers=headers, params=query)
                results = response.json()['data']
                for res in results:
                    if type(res['availability']['seats']) == int:
                        if res['price'] < flight.price:
                            flight.price = res['price']
                            flight.save()

                            with smtplib.SMTP_SSL(MAIL_PROVIDER_SMTP_ADDRESS, 465) as connection:
                                connection.login(MY_EMAIL, MY_PASSWORD)
                                connection.sendmail(
                                    from_addr=MY_EMAIL,
                                    to_addrs=flight.user.email,
                                    msg=f"Subject:TAŃSZY LOT!!! \n\n{flight.origin_airport_text} -  {flight.destination_airport_text} nowa cena: {flight.price} pln \n {res['deep_link']}".encode('utf-8'))
                            break

        except FlightData.DoesNotExist:
            raise CommandError('FlightData does not exist')



