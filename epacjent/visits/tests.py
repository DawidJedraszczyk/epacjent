from django.test import TestCase
from django.urls import reverse, resolve
from . import views
from django.contrib.auth.models import User
from .models import Visit
import uuid
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

class VisitsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        cls.visit = Visit.objects.create(
            user=cls.user,
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

