from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from event.models import Event, Category
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from weather_api.weather import get_weather_context
from django.db.models import OuterRef, Subquery

@login_required
def new_conversation(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    categories = Category.objects.all()

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    if event.created_by == request.user:
        return redirect('user:profile', username=request.user.username)
    
    conversations = Conversation.objects.filter(event=event).filter(members__in=[request.user.id])

    if conversations:
        return redirect('communication:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(event=event)
            conversation.members.add(request.user)
            conversation.members.add(event.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('event:event_detail', pk=event_pk)

    else:
        form = ConversationMessageForm()
    
    return render(request, 'communication/new_conversation.html', {
        'form': form,
        'event': event,
        'categories': categories,
        'title': 'New Conversation',
        **context
    })

@login_required
def inbox(request):
    # conversations = Conversation.objects.filter(members__in=[request.user.id]).order_by('-modified_at')

    latest_message_subquery = ConversationMessage.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-created_at').values('content')[:1]

    conversations = Conversation.objects.filter(
        members__in=[request.user.id]
    ).order_by('-modified_at').annotate(
        latest_message_content=Subquery(latest_message_subquery)
    )
    
    latest_message_timestamp_subquery = ConversationMessage.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-created_at').values('created_at')[:1]
    
    conversations = conversations.annotate(
        latest_message_timestamp=Subquery(latest_message_timestamp_subquery)
    )
    categories = Category.objects.all()

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    return render(request, 'communication/inbox.html', {
        'conversations': conversations,
        'categories': categories,
        'title': 'Inbox',
        **context
    })

@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members__in=[request.user.id])
    categories = Category.objects.all()

    location = '51.5072,-0.1276'
    context = get_weather_context(location)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('communication:detail', pk=pk)

    else:
        form = ConversationMessageForm()
    
    return render(request, 'communication/conversation_detail.html', {
        'conversation': conversation,
        'form': form,
        'categories': categories,
        'title': 'Conversation',
        **context
    })