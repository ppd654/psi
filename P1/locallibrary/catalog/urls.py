from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path(
        'book/<int:pk>',
        views.BookDetailView.as_view(),
        name='book-detail'
    ),
    path(
        'book/<uuid:pk>/renew/',
        views.renew_book_librarian,
        name='renew-book-librarian'
    ),
    path(
        'borrowed/',
        views.AllBorrowedListView.as_view(),
        name='all-borrowed'
    ),

    # Herramientas de Autor
    path(
        'author/create/',
        views.AuthorCreateView.as_view(),
        name='author-create'
    ),
    path(
        'author/<int:pk>/update/',
        views.AuthorUpdate.as_view(),
        name='author-update'
    ),
    path(
        'author/<int:pk>/delete/',
        views.AuthorDelete.as_view(),
        name='author-delete'
    ),
    path(
        'author/<int:pk>',
        views.AuthorDetailView.as_view(),
        name='author-detail'
    ),
    path('authors/', views.AuthorListView.as_view(), name='authors'),

    # Herramientas de Libro
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path(
        'book/<int:pk>/update/',
        views.BookUpdate.as_view(),
        name='book-update'
    ),
    path(
        'book/<int:pk>/delete/',
        views.BookDelete.as_view(),
        name='book-delete'
    ),

    # Libros prestados (Usuario actual)
    path(
        'mybooks/',
        views.LoanedBooksByUserListView.as_view(),
        name='my-borrowed'
    ),
]
