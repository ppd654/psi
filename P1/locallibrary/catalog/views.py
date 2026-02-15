from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstance, Author, Genre
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

from catalog.forms import RenewBookForm

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
class BookDetailView(generic.DetailView):
    model = Book

def renew_book_librarian(request, pk):
    """Vista para que los bibliotecarios renueven un BookInstance específico."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Si se trata de una petición POST, procesamos los datos del formulario
    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos recibidos
        form = RenewBookForm(request.POST)

        # Comprobamos si el formulario es válido (aquí se ejecuta tu clean_renewal_date)
        if form.is_valid():
            # Procesamos los datos en form.cleaned_data y actualizamos la base de datos
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirigimos a una nueva URL (por ejemplo, a la lista de todos los libros prestados)
            return HttpResponseRedirect(reverse('index')) # Por ahora a la home

    # Si es un GET (o cualquier otro método), creamos el formulario por defecto
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



from django.contrib.auth.mixins import PermissionRequiredMixin

class AllBorrowedListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan to all users."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Muestra todos los campos del modelo

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors') # Al borrar, vuelve a la lista de autores

class AuthorDetailView(generic.DetailView):
    model = Author

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
