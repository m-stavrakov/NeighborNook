from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventImage, Category
from .forms import NewEventForm, EventImageForm, EditEventForm, EventImageFormSet
from django.forms import modelformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from weather_api.weather import get_weather_context

# Event Creation
@login_required
def new_event(request):
    ImageFormSet = modelformset_factory(EventImage, form=EventImageForm, extra=10, max_num=10)
    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    if request.method == 'POST':
        event_form = NewEventForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=EventImage.objects.none())

        if event_form.is_valid() and image_formset.is_valid():
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()

            for form in image_formset.cleaned_data:
                if form:
                    image = form['image']
                    EventImage(event=event, image=image).save()

            return redirect('home:home_loggedin')
    else:
        event_form = NewEventForm()
        image_formset = ImageFormSet(queryset=EventImage.objects.none())

    return render(request, 'event/event.html', {
        'form': event_form,
        'image_formset': image_formset,
        'title': 'New Event',
        'button_text': 'Create Event',
        **context
    })

# Event Categories
def events_categories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    events = Event.objects.filter(category=category, is_active=True).order_by('-date')

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'event/events_category.html', {
        'events': events,
        'category': category,
        **context
    })

# Event Details
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'event/event_details.html', {
        'event': event,
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
    
    return render(request, 'item/items_search.html', {
        'events': events,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        **context
    })

# Event Delete
@login_required
def delete_event(request, pk):
    item = get_object_or_404(Event, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

# Event Update
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)

    location = '51.5072,-0.1276'
    weather = get_weather_context(location)

    if request.method == 'POST':
        event_form = EditEventForm(request.POST, instance=event)
        formset = EventImageFormSet(request.POST, request.FILES, queryset=EventImage.objects.filter(event=event))

        if event_form.is_valid() and formset.is_valid():
            event_form.save()
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                else:
                    image_instance = form.save(commit=False)
                    image_instance.event = event
                    image_instance.save()
            return redirect('event_detail', pk=event.pk)
    else:
        event_form = EditEventForm(instance=event)
        formset = EventImageFormSet(queryset=EventImage.objects.filter(event=event))

    context = {
        'event_form': event_form,
        'formset': formset,
        'title': 'Edit Event',
        'button_text': 'Update Event'
    }

    full_context = {**context, **weather}

    return render(request, 'event/event.html', full_context)