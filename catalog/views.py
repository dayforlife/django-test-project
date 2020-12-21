from django.http import Http404
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.
    num_genres = Genre.objects.count()
    books_with_title = ', '.join(map(str, Book.objects.filter(title__icontains='the')[:5]))

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    # return render(
    #     request,
    #     'index.html',
    #     context={'num_books': num_books, 'num_instances': num_instances,
    #              'num_instances_available': num_instances_available, 'num_authors': num_authors,
    #              'num_genres': num_genres, 'books_with_title': books_with_title}
    # )
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    # context_object_name = 'my_book_list'  # ваше собственное имя переменной контекста в шаблоне
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # Получение 5 книг, содержащих слово 'war' в заголовке
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Определение имени вашего шаблона и его расположения



    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='the')[:5]  # Получить 5 книг, содержащих 'war' в заголовке
    #
    # def get_context_data(self, **kwargs):
    #     # В первую очередь получаем базовую реализацию контекста
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Добавляем новую переменную к контексту и иниуиализируем ее некоторым значением
    #     context['some_data'] = 'This is just some data'
    #     return context

class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        # book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'catalog/book_detail.html',
            context={'book': book_id, }
        )

class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    print(queryset)


class AuthorDetailView(generic.DetailView):
    model = Author

    def book_detail_view(request, pk):
        try:
            author_id = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        # book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'catalog/author_detail.html',
            context={'author': author_id, }
        )
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')