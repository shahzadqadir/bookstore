from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from books.models import Book, Review
from books.views import BookListView, BookDetailView

class TestBookModel(TestCase):

    def setUp(self):
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
        url = reverse('book_list')
        self.response = self.client.get(url)

    def test_book_list_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
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
        self.response = self.client.get(self.book.get_absolute_url())


    def test_book_detail_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_book_detail_template(self):
        self.assertTemplateUsed('books/book_detail')

    def test_book_detail_view(self):
        view = resolve(self.book.get_absolute_url())
        self.assertEqual(
            view.func.__name__,
            BookDetailView.as_view().__name__
        )

    def test_book_detail_content(self):
        self.assertContains(self.response, 'Atomic Habbits')


class TestReviews(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title='test title', author='test author 1', price=10.10)
        author = get_user_model().objects.create(username='test123', email='test123@gmail.com', password='test123')
        self.review = Review.objects.create(
            book=self.book,
            review='this is only a test comment',
            author=author
        )
        self.response = self.client.get(self.book.get_absolute_url())

    def test_review_creation(self):
        self.assertEqual(self.review.book.title, 'test title')
        self.assertEqual(self.review.book.author, 'test author 1')
        self.assertEqual(self.review.book.price, 10.10)
        self.assertEqual(self.review.author.username, 'test123')
        self.assertEqual(self.review.review, 'this is only a test comment')

    def test_number_of_reviews(self):
        self.assertEqual(len(self.book.reviews.all()), 1)

    def test_book_contain_review(self):
        self.assertContains(self.response, 'this is only a test comment')
