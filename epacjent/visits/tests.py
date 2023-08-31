from django.test import TestCase, Client
from django.urls import reverse, resolve
from . import views
from django.contrib.auth.models import User
from .models import Visit
from datetime import datetime, timedelta
import uuid
from .forms import VisitForm  # Import your VisitForm
class TestUrls(TestCase):
    def test_index_url_is_resolved(self):
        url = reverse('visits:visitsPanel')
        self.assertEquals(resolve(url).func.view_class, views.Index)

    def test_visit_url_is_resolved(self):
        url = reverse('visits:visit', kwargs={'pk': '6191fe11-1d7b-436f-bf25-21e858c6af5e'})
        self.assertEquals(resolve(url).func.view_class, views.VisitView)

    def test_create_visit_url_is_resolved(self):
        url = reverse('visits:create-visit')
        self.assertEquals(resolve(url).func.view_class, views.CreateVisitView)

    def test_update_visit_url_is_resolved(self):
        url = reverse('visits:update-visit', kwargs={'pk': '6191fe11-1d7b-436f-bf25-21e858c6af5e'})
        self.assertEquals(resolve(url).func.view_class, views.UpdateVisitView)

    def test_cancel_visit_url_is_resolved(self):
        url = reverse('visits:cancel-visit', kwargs={'pk': '6191fe11-1d7b-436f-bf25-21e858c6af5e'})
        self.assertEquals(resolve(url).func.view_class, views.CancelVisitView)

    def test_send_mail_url_is_resolved(self):
        url = reverse('visits:send-mail', kwargs={'pk': '6191fe11-1d7b-436f-bf25-21e858c6af5e'})
        self.assertEquals(resolve(url).func.view_class, views.Send_mail)

class TestModels(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.visit = Visit.objects.create(
            user=self.user,
            name='Test Visit',
            description='This is a test visit.',
            visit_date='2023-08-30',
            visit_hour='14:30:00'
        )

    def test_str_representation(self):
        self.assertEqual(str(self.visit), 'Test Visit')

    def test_visit_model_fields(self):
        self.assertEqual(self.visit.user, self.user)
        self.assertEqual(self.visit.name, 'Test Visit')
        self.assertEqual(self.visit.description, 'This is a test visit.')
        self.assertEqual(self.visit.visit_date, '2023-08-30')
        self.assertEqual(self.visit.visit_hour, '14:30:00')

    def test_created_and_updated_fields(self):
        self.assertIsNotNone(self.visit.created)
        self.assertIsNotNone(self.visit.updated)

    def test_id_field_is_uuid(self):
        self.assertIsNotNone(self.visit.id)
        self.assertTrue(isinstance(self.visit.id, uuid.UUID))

    def test_default_visit_date_and_hour(self):
        new_visit = Visit.objects.create(
            user=self.user,
            name='Another Test Visit',
            description='Another test visit without specifying date and hour.'
        )
        self.assertIsNone(new_visit.visit_date)
        self.assertIsNone(new_visit.visit_hour)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.visits_panel_url = reverse('visits:visitsPanel')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.visit_form_data = {
            'name': 'Test Visit',
            'description': 'Test Description',
            'visit_date': (datetime.now() + timedelta(days=1)).date(),  # Tomorrow's date
            'visit_hour': '10:00',  # Assuming this is the format
        }
    def test_visits_panel_without_login_GET(self):
        response = self.client.get(self.visits_panel_url)
        self.assertEquals(response.status_code, 302) #redirected to login

    def test_visits_panel_user_GET(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.visits_panel_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'visits.html')

    def test_get_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('visits:create-visit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createVisit.html')
        self.assertIsInstance(response.context['form'], VisitForm)

    def test_valid_post_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('visits:create-visit'), data=self.visit_form_data)
        self.assertEqual(response.status_code, 302)  # Redirect expected on success
        self.assertRedirects(response, reverse('visits:visitsPanel'))
        self.assertEqual(Visit.objects.count(), 1)  # Check if a Visit object was created

    def test_invalid_past_date_post_request(self):
        self.client.login(username='testuser', password='testpassword')
        self.visit_form_data['visit_date'] = (datetime.now() - timedelta(days=1)).date()  # Yesterday's date
        response = self.client.post(reverse('visits:create-visit'), data=self.visit_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createVisit.html')
        self.assertIn('Invalid inputs', response.content.decode('utf-8'))
        self.assertEqual(Visit.objects.count(), 0)  # No Visit object should be created

    def test_missing_date_post_request(self):
        self.client.login(username='testuser', password='testpassword')
        self.visit_form_data.pop('visit_date')
        response = self.client.post(reverse('visits:create-visit'), data=self.visit_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('visits:visitsPanel'))
        self.assertEqual(Visit.objects.count(), 1)  # Visit object should be created without date
