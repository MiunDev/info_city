import requests
from django.shortcuts import render
from info_city.models import City
from .forms import CityForm


def index(request):
    appid = '959b2d9a142ead220f2b9951479411a9'
    url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=' + appid

    if (request.method == 'POST'):
        form = CityForm(request.POST)  # request.POST == значения которые получаем от пользователя из формы
        form.save()  # сохранение данных в БД

    form = CityForm()  # очистка формы

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()  # из json в формат словарей

        city_info = {
            'city': city.name,
            'temp': res["list"][0]["main"]["temp"],
            'icon': res["list"][0]["weather"][0]["icon"]
        }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'info_city/index.html', context)
