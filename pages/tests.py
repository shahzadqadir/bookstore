from django.test import SimpleTestCase

from django.urls import reverse, resolve

from pages.views import HomePageView


class HomePageTests(SimpleTestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_homepage_status_code(self):        
        self.assertEqual(200, self.response.status_code)

    def test_homepage_url_name(self):
        self.assertEqual(200, self.client.get(reverse('home')).status_code)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Homepage')

    def test_homepage_not_contains_html(self):
        self.assertNotContains(self.response, 'Something not expected.')

    def test_homepage_url_resolves_homepage_view(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )

class AboutPageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_about_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_template_used(self):
        self.assertTemplateUsed(self.response, 'pages/about.html')

    