from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventImage, Category
from .forms import NewEventForm, EventImageForm, EditEventForm
from django.forms import modelformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from weather_api.weather import get_weather_context
from django.contrib import messages

# Event Creation
@login_required
def new_event(request):
    ImageFormSet = modelformset_factory(EventImage, form=EventImageForm, extra=0, can_delete=True)
    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    if request.method == 'POST':
        event_form = NewEventForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=EventImage.objects.none())

        if event_form.is_valid() and image_formset.is_valid():
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()

            for file in request.FILES.getlist('image'):
                EventImage.objects.create(event=event, image=file)

            for form in image_formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                else:
                    image_instance = form.save(commit=False)
                    image_instance.event = event
                    image_instance.save()

            return redirect('home:home')
    else:
        event_form = NewEventForm()
        image_formset = ImageFormSet(queryset=EventImage.objects.none())
    
    event_fields_col1 = ['name', 'overview', 'description']
    event_fields_col2 = ['location', 'date', 'time', 'category', 'age_limit', 'weather', 'what_to_bring']

    categories = Category.objects.all()

    return render(request, 'event/event.html', {
        'form': event_form,
        'image_formset': image_formset,
        'title': 'New Event',
        'button_text': 'Create Event',
        'event_fields_col1': event_fields_col1,
        'event_fields_col2': event_fields_col2,
        'categories': categories,
        **context
    })

# Event Categories
def events_categories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    events = Event.objects.filter(category=category, is_active=True).order_by('-date')
    categories = Category.objects.all()

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'event/events_category.html', {
        'events': events,
        'category': category,
        'title': category.name,
        'categories': categories,
        **context
    })

# Event Details
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    categories = Category.objects.all()
    related_events = Event.objects.filter(category=event.category, is_active=True).exclude(pk=pk) [:3]

    event_age_limit = event.age_limit

    if event_age_limit == 0:
        event_age_limit = 'All ages!'
    elif event_age_limit == 13:
        event_age_limit = '13+'
    elif event_age_limit == 18:
        event_age_limit = '18+'
    elif event_age_limit == 21:
        event_age_limit = '21+'
    elif event_age_limit == 50:
        event_age_limit = '50+'
    else:
        event_age_limit = 'Unknown'

    event_weather = event.weather

    if event_weather == 'sunny':
        event_weather = 'Sunny'
    elif event_weather == 'rainy':
        event_weather = 'Rainy'
    elif event_weather == 'cloudy':
        event_weather = 'Cloudy'
    elif event_weather == 'snowy':
        event_weather = 'Snowy'
    else:
        event_weather = 'Unknown'

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'event/event_details.html', {
        'event': event,
        'categories': categories,
        'related_events': related_events,
        'title': event.name,
        'event_age_limit': event_age_limit,
        'event_weather': event_weather,
        **context
    })

# Event Search
def event_search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    events = Event.objects.filter(is_active=True).order_by('-date')

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    if category_id:
        events = events.filter(category_id=category_id)
    
    if query:
        events = events.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'event/events_search.html', {
        'events': events,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'title': 'Search Events',
        **context
    })

# Event Delete
@login_required
def delete_event(request, pk):
    item = get_object_or_404(Event, pk=pk, created_by=request.user)
    item.delete()

    messages.success(request, 'Event deleted successfully.')

    return redirect('user:profile', username=request.user.username)

# Event Update
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)

    
    location = '51.5072,-0.1276'
    weather = get_weather_context(location)
    categories = Category.objects.all()

    if request.method == 'POST':
       
        event_form = EditEventForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()
            return redirect('event:event_detail', pk=event.pk)
    else:
        
        event_form = EditEventForm(instance=event)

    context = {
        'event_form': event_form,
        'title': 'Edit Event',
        'button_text': 'Update Event',
        'categories': categories
    }

    full_context = {**context, **weather}

    return render(request, 'event/event_update.html', full_context)
