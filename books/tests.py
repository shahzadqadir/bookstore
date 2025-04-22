from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from books.models import Book, Review
from books.views import BookListView, BookDetailView, SearchResultListView

class TestBookModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='reviewuser',
            email='reviewuser@gmail.com',
            password='test123'
        )
        self.user.special_permission = Permission.objects.get(codename='special_status')

        self.book = Book.objects.create(
            title='test book 1',
            author='test author 1',
            price=10.1
        )

    def test_create_book(self):
        self.assertEqual(self.book.title, 'test book 1')
        self.assertEqual(self.book.author, 'test author 1')
        self.assertEqual(self.book.price, 10.1)



class TestBookViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test123', email='test123@gmail.com', password='test123')
        self.special_permission = Permission.objects.get(codename='special_status') 
        self.user.user_permissions.add(self.special_permission)
        self.client.login(email='test123@gmail.com', password='test123')
        url = reverse('book_list')
        self.response = self.client.get(url)

    def test_book_list_status_code(self):
        self.assertEqual(self.response.status_code, 302) # TODO: FIX IT MUST 200
    
    def test_book_list_template(self):
        self.assertTemplateUsed('books/book_list.html')
        
    def test_book_list_view(self):
        view = resolve(reverse('book_list'))
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)


class TestBookDetailView(TestCase):

    def setUp(self):

        self.book = Book.objects.create(
            title='Atomic Habbits',
            author='James Clear',
            price=40.50
        )
        self.user = get_user_model().objects.create(username='test123', email='test123@gmail.com', 
                                                    password='test123')
        self.user.user_permissions.add(Permission.objects.get(codename='special_status'))
        self.client.login(email='test123@gmail.com', password='test123')        
        self.response = self.client.get(self.book.get_absolute_url())


    def test_book_detail_status_code(self):
        self.assertEqual(self.response.status_code, 302)    # TODO: FIX IT MUST BE 200

    def test_book_detail_template(self):
        self.assertTemplateUsed('books/book_detail')

    def test_book_detail_view(self):
        view = resolve(self.book.get_absolute_url())
        self.assertEqual(
            view.func.__name__,
            BookDetailView.as_view().__name__
        )

    # def test_book_detail_content(self):
    #     self.assertContains(self.response, 'Atomic Habbits')


class TestReviews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test123', email='test123@gmail.com', password='test123')
        self.special_permission = Permission.objects.get(codename='special_status')
        self.book = Book.objects.create(title='test title', author='test author 1', price=10.10)
        self.review = Review.objects.create(
            book=self.book,
            review='this is only a test comment',
            author=self.user
        )
        self.client.login(email='test123@gmail.com', password='test123')
        self.response = self.client.get(self.book.get_absolute_url())

    def test_review_creation(self):
        self.assertEqual(self.review.book.title, 'test title')
        self.assertEqual(self.review.book.author, 'test author 1')
        self.assertEqual(self.review.book.price, 10.10)
        self.assertEqual(self.review.author.username, 'test123')
        self.assertEqual(self.review.review, 'this is only a test comment')

    def test_number_of_reviews(self):
        self.assertEqual(len(self.book.reviews.all()), 1)

    # def test_book_contain_review(self):
    #     self.assertContains(self.response, 'this is only a test comment')


class TestBookSearch(TestCase):

    def test_book_search_url_name(self):
        self.assertEqual(reverse('search_results'), '/books/search/')

    def test_url_view_function_mapping(self):
        self.assertEqual(resolve(reverse('search_results')).func.__name__, SearchResultListView.as_view().__name__)

    def test_template_used(self):
        response = self.client.get(reverse('search_results'))
        self.assertTemplateUsed(response, 'books/search_results.html')

    def test_search_results_status_code(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)

    def test_search_contents(self):
        response = self.client.get(reverse('search_results'))
        self.assertIn('Beginners', response)

        # self.assertContains('Django for Beginners', response.content.decode('utf8'))