from django.db.models import Count
import requests
from main.models import *

WEATHER_API_KEY = '90a715f25c03464b96a182044251512'
WEATHER_CITY = "fergana"


def get_categories(request):
    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).order_by('-articles_count')[:15]
    return {'categories': categories}

def get_weather(request):

    weather_data = requests.get(
        f"https://api.weatherapi.com/v1/current.json?q={WEATHER_CITY}&key={WEATHER_API_KEY}"
    ).json()
    weather = {
        'temp': weather_data['current']['temp_c'],
        'conditions': weather_data['current']['condition'],
        'time': weather_data['location']['localtime'],
    }

    return {
        'weather': weather,
    }