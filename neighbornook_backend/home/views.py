from django.shortcuts import render
from event.models import Event, Category
from weather_api.weather import get_weather_context

def home(request):
    location = '51.5072,-0.1276'
    context = get_weather_context(location)
    user = request.user

    if user.is_authenticated:
            events = Event.objects.filter(is_active=True).order_by('-date')[:6]
            categories = Category.objects.all()

            context.update({
                'events': events,
                'categories': categories,
            })
            template = 'home/home_loggedin.html'
    else:
            template = 'home/home_not_loggedin.html'


    return render(request, template, {
        'user': request.user,
        **context
    })