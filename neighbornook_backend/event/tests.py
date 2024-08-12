from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from event.models import Event, EventImage, Category
from event.forms import NewEventForm, EditEventForm, EventImageFormSet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

class NewEventViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.location = '51.5072,-0.1276'

    def test_create_event_with_images(self):
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('event:new_event'), {
            'name': 'Test Event',
            'overview': 'Overview of the event',
            'description': 'Description of the event',
            'location': 'Location of the event',
            'date': '2024-12-31',
            'time': '14:00',
            'category': self.category.pk,
            'age_limit': 18,
            'weather': 'Sunny',
            'what_to_bring': 'Nothing',
            'image-TOTAL_FORMS': 1,
            'image-INITIAL_FORMS': 0,
            'image-MAX_NUM_FORMS': 1,
            'image-0-image': image_file,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        event = Event.objects.first()
        self.assertTrue(Event.objects.exists())
        self.assertTrue(EventImage.objects.filter(event=event).exists())

    def test_create_event_form_errors(self):
        response = self.client.post(reverse('event:new_event'), {
            'name': '',  # Invalid data
            'overview': '',
            'description': '',
            'location': '',
            'date': '',
            'time': '',
            'category': '',
            'age_limit': '',
            'weather': '',
            'what_to_bring': '',
        })
        self.assertEqual(response.status_code, 200)  # Form errors should return to the same page
        self.assertFormError(response, 'form', 'name', 'This field is required.')

class EventsCategoriesViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.event = Event.objects.create(
            name='Test Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-31',
            time='14:00',
            category=self.category,
            created_by=self.user,
            age_limit=18,
            weather='Sunny',
            what_to_bring='Nothing'
        )

    def test_view_category_events(self):
        response = self.client.get(reverse('event:events_categories', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertContains(response, self.category.name)

class EventDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.event = Event.objects.create(
            name='Test Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-31',
            time='14:00',
            category=self.category,
            created_by=self.user,
            age_limit=18,
            weather='Sunny',
            what_to_bring='Nothing'
        )
        self.related_event = Event.objects.create(
            name='Related Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-30',
            time='14:00',
            category=self.category,
            created_by=self.user,
            age_limit=18,
            weather='Rainy',
            what_to_bring='Nothing'
        )

    def test_event_detail_view(self):
        response = self.client.get(reverse('event:event_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.name)
        self.assertContains(response, self.related_event.name)

class EventSearchViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.event = Event.objects.create(
            name='Test Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-31',
            time='14:00',
            category=self.category,
            created_by=self.user,
            age_limit=18,
            weather='Sunny',
            what_to_bring='Nothing'
        )

    def test_event_search(self):
        response = self.client.get(reverse('event:event_search'), {'query': 'Test Event'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'Search Events')

    def test_search_by_category(self):
        response = self.client.get(reverse('event:event_search'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'Test Event')

class DeleteEventViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.event = Event.objects.create(
            name='Test Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-31',
            time='14:00',
            created_by=self.user,
            age_limit=18,
            weather='Sunny',
            what_to_bring='Nothing'
        )

    def test_delete_event(self):
        response = self.client.post(reverse('event:delete_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())
        self.assertContains(response, 'Event deleted successfully.')

class EditEventViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.event = Event.objects.create(
            name='Test Event',
            overview='Overview',
            description='Description',
            location='Location',
            date='2024-12-31',
            time='14:00',
            category=self.category,
            created_by=self.user,
            age_limit=18,
            weather='Sunny',
            what_to_bring='Nothing'
        )

    def test_edit_event(self):
        response = self.client.post(reverse('event:edit_event', kwargs={'pk': self.event.pk}), {
            'name': 'Updated Event',
            'overview': 'Updated Overview',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'date': '2024-12-31',
            'time': '14:00',
            'category': self.category.pk,
            'age_limit': 21,
            'weather': 'Rainy',
            'what_to_bring': 'Updated Items'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')
        self.assertEqual(self.event.weather, 'Rainy')
