from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from event.models import Event, Category
from communication.models import Conversation, ConversationMessage
from communication.forms import ConversationMessageForm
from django.utils import timezone

class NewConversationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.event = Event.objects.create(title='Test Event', created_by=self.other_user)
        self.category = Category.objects.create(name='Test Category')
        self.event.categories.add(self.category)
        self.client.login(username='testuser', password='password')

    def test_redirect_if_user_is_event_creator(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('communication:new_conversation', args=[self.event.pk]))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': 'otheruser'}))

    def test_redirect_if_conversation_exists(self):
        conversation = Conversation.objects.create(event=self.event)
        conversation.members.add(self.user, self.other_user)
        response = self.client.get(reverse('communication:new_conversation', args=[self.event.pk]))
        self.assertRedirects(response, reverse('communication:detail', kwargs={'pk': conversation.pk}))

    def test_create_conversation_and_message(self):
        response = self.client.post(reverse('communication:new_conversation', args=[self.event.pk]), {
            'content': 'Hello World'
        })
        conversation = Conversation.objects.first()
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Conversation.objects.exists())
        self.assertTrue(ConversationMessage.objects.filter(content='Hello World').exists())
        self.assertRedirects(response, reverse('event:event_detail', kwargs={'pk': self.event.pk}))

class InboxViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.event = Event.objects.create(title='Test Event', created_by=self.other_user)
        self.conversation = Conversation.objects.create(event=self.event)
        self.conversation.members.add(self.user, self.other_user)
        self.client.login(username='testuser', password='password')

    def test_inbox_view(self):
        response = self.client.get(reverse('communication:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inbox')
        self.assertContains(response, self.event.title)
        self.assertContains(response, self.user.username)

class DetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.event = Event.objects.create(title='Test Event', created_by=self.other_user)
        self.conversation = Conversation.objects.create(event=self.event)
        self.conversation.members.add(self.user, self.other_user)
        self.client.login(username='testuser', password='password')

    def test_access_existing_conversation(self):
        response = self.client.get(reverse('communication:detail', kwargs={'pk': self.conversation.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conversation')
        self.assertContains(response, self.event.title)

    def test_access_non_member_conversation(self):
        new_user = User.objects.create_user(username='newuser', password='password')
        self.client.login(username='newuser', password='password')
        response = self.client.get(reverse('communication:detail', kwargs={'pk': self.conversation.pk}))
        self.assertEqual(response.status_code, 404)  # Not found if user is not a member