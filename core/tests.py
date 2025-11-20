from django.test import TestCase
from django.urls import reverse
LANGUAGE_SESSION_KEY = 'django_language'

from .models import (
    CardBlock,
    Footer,
    Hero,
    NavigationItem,
    Section,
    SiteSettings,
)


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.settings = SiteSettings.objects.create(site_name="Test Site")
        cls.hero = Hero.objects.create(title="Hero Title", is_active=True)
        cls.section = Section.objects.create(name="Highlights", is_active=True)
        cls.card = CardBlock.objects.create(
            section=cls.section,
            title="First Card",
            cta_label="Learn More",
            cta_url="https://example.com",
        )
        cls.nav_item = NavigationItem.objects.create(
            label="About",
            url="about",
            is_active=True,
        )
        cls.footer = Footer.objects.create(description="Footer text", is_active=True)

    def test_home_renders_active_content(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.settings.site_name)
        self.assertIn('hero', response.context)
        self.assertIn('sections', response.context)
        self.assertGreaterEqual(response.context['sections'].count(), 1)

    def test_track_card_click_updates_counter(self):
        url = reverse('track_card_click', args=[self.card.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.card.refresh_from_db()
        self.assertEqual(self.card.click_count, 1)

    def test_language_parameter_sets_session(self):
        response = self.client.get(reverse('home'), {'lang': 'am'})
        session = self.client.session
        self.assertEqual(session[LANGUAGE_SESSION_KEY], 'am')
        self.assertEqual(response.wsgi_request.LANGUAGE_CODE, 'am')


class CardBlockPayloadTests(TestCase):
    def test_payload_accessors(self):
        section = Section.objects.create(name="Dynamic")
        card = CardBlock.objects.create(
            section=section,
            title="Flexible Card",
            payload={
                'role': 'Engineer',
                'feature_list': ['One', 'Two'],
                'is_featured': True,
            }
        )
        self.assertTrue(card.has_type_specific_data())
        self.assertEqual(card.get_payload_value('role'), 'Engineer')
        self.assertEqual(card.get_payload_list('feature_list'), ['One', 'Two'])
        self.assertEqual(card.get_payload_value('missing', 'fallback'), 'fallback')
