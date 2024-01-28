from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from dateutil import parser
from search_app.forms import LoginForm, UserForm
from search_app.models import FlightData, Category

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2"
TEQUILA_API_KEY = "Q_vLi3x_VS-0ze9glMSWHCWOmr7VxZB3"


class StartView(View):
    """application start view. sets departure and return dates to default values. the user can change them"""
    def get(self, request):
        day_now = date.today()
        day_to = date.today()+relativedelta(months=1)
        ctx = {
            "day_now": day_now.strftime("%Y-%m-%d"),
            "day_to": day_to.strftime("%Y-%m-%d")
        }
        return render(request, "start.html", ctx)

class SearchView(View):
    """In the get function, TEQUILA_API_KEY query to search for the flight selected by the user.
    It uses the SEARCH API function and the SearchDestinationCode class to search for airport codes
    in the post function for logged in users, it allows you to post searched flights."""

    def get(self, request):
        location_endpoint = f"{TEQUILA_ENDPOINT}/search"
        headers = {"apikey": TEQUILA_API_KEY}
        date_from = parser.parse(request.GET['date_from']).strftime('%d/%m/%Y')
        date_to = parser.parse(request.GET['date_to']).strftime('%d/%m/%Y')
        return_from = parser.parse(request.GET['return_from']).strftime('%d/%m/%Y')
        return_to = parser.parse(request.GET['return_to']).strftime('%d/%m/%Y')

        query = {
            "fly_from": request.GET['origin_airport'],
            "fly_to": request.GET['destination_airport'],
            "adults": request.GET['adults'],
            "children": request.GET['children'],
            "infants": request.GET['infants'],
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
        results_seats = []
        for res in results:
            if type(res['availability']['seats']) == int:
                res['route'][0]['local_departure'] = parser.parse(res['route'][0]['local_departure']).strftime('%d/%m/%Y  %H:%M')
                res['route'][1]['local_departure'] = parser.parse(res['route'][1]['local_departure']).strftime('%d/%m/%Y  %H:%M')
                results_seats.append(res)

        ctx = {
            "fly_from": request.GET['origin_airport_text'],
            "fly_to": request.GET['destination_airport_text'],
            "results": results_seats,
        }

        if self.request.user.is_authenticated:
            return render(request, "user_search_result.html", ctx)
        return render(request, "search_result.html", ctx)

    def post(self, request):
        fly_from = request.GET['origin_airport']
        origin_airport_text = request.GET['origin_airport_text']
        fly_to = request.GET['destination_airport']
        destination_airport_text = request.GET['destination_airport_text']
        adults = request.GET['adults']
        children = request.GET['children']
        infants = request.GET['infants']
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        return_from = request.GET['return_from']
        return_to = request.GET['return_to']
        price = request.POST.get('price')
        user = self.request.user
        categories = request.POST.get('categories')
        new_cat = Category.objects.filter(category_name=categories).first()

        print(request.POST)


        search_save = FlightData.objects.create(
            fly_from=fly_from,
            origin_airport_text=origin_airport_text,
            fly_to=fly_to,
            destination_airport_text=destination_airport_text,
            adults=adults,
            children=children,
            infants=infants,
            date_from=date_from,
            date_to=date_to,
            return_from=return_from,
            return_to=return_to,
            price=price,
            user=user,
        )
        search_save.save()
        search_save.categories.add(new_cat)

        ctx = {
            "fly_from": request.GET['origin_airport_text'],
            "fly_to": request.GET['destination_airport_text'],
            "price": price
        }

        return render(request, "save_search.html", ctx)






class LoginView(FormView):
    """user login. will use django's built-in functionality and automatic User tables. The forms.py file contains the data that will be required"""

    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/')


class AddUser(FormView):
    """will use django's built-in functionality to create automatic User tables. The forms.py file contains the data that will be required and saved"""

    template_name = "add_user_form.html"
    form_class = UserForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email)
        new_user.save()
        return super().form_valid(form)


class SearchDestinationCode(View):

    def get(self, request):
        """finding airport codes and names using a connection with TEQUILA_API"""

        TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
        TEQUILA_API_KEY = "Q_vLi3x_VS-0ze9glMSWHCWOmr7VxZB3"

        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": request.GET['q'], "locale": "pl-PL", "location_types": "airport", "limit": "10", "active_only": "true"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]

        city_names = [{'value': row["code"], 'text': row['name']} for row in results]

        return JsonResponse(city_names, safe=False)


class SaveHistoryView(View):
    """for logged in users, it shows saved flight searches"""
    def get(self, request):
        flight = FlightData.objects.filter(user=self.request.user.id)

        return render(request, "save_history.html", {"flight": flight})
