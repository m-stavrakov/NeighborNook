from django.shortcuts import render
from event.models import Event, EventImage, Category
from weather_api.weather import get_weather_context

def home(request):
    location = '51.5072,-0.1276'
    context = get_weather_context(location)


    return render(request, 'home/home_not_loggedin.html', {
            'user': request.user,
            **context
        })

def home_loggedin(request):
    events = Event.objects.filter(is_active=True).order_by('-date') [0:6]
    categories = Category.objects.all()

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'home/home_loggedin.html', {
            **context,
            'user': request.user,
            'events': events,
            'categories': categories,
        })