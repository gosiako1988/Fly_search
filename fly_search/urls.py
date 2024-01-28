"""
URL configuration for fly_search project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from search_app.views import StartView, SearchView, LoginView, logout_view, AddUser, SearchDestinationCode, SaveHistoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartView.as_view(), name="/"),
    path('search/', SearchView.as_view(), name="search"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_user/', AddUser.as_view(), name='add_user'),
    path('search_destination_code', SearchDestinationCode.as_view(), name='city_code'),
    path('save/history/', SaveHistoryView.as_view(), name='save_history'),

]
