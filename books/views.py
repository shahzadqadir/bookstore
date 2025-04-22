from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from books.models import Book

from django.db.models import Q

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"
    login_url = "account_login"


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    permission_required = 'books.special_status'


class SearchResultListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"
    
    def get_queryset(self):
        return Book.objects.filter(Q(title__icontains=self.request.GET.get('search')) | Q(author__icontains=self.request.GET.get('search')))