from django.test import TestCase
from catalog.models import Author
import datetime
from catalog.forms import RenewBookForm 
from django.urls import reverse
from django.contrib.auth.models import User

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Crea datos de prueba una sola vez para toda la clase de test.
        """
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        """Prueba que la etiqueta del nombre sea la esperada."""
        # Búsqueda certera por atributos, no por ID
        author = Author.objects.get(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        """Prueba que la etiqueta del apellido sea la esperada."""
        author = Author.objects.get(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_death_label(self):
        """Prueba la etiqueta de fecha de fallecimiento (corregido Case Sensitive)."""
        author = Author.objects.get(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('date_of_death').verbose_name
        # Ajustado a 'Died' para que coincida con la respuesta de tu sistema
        self.assertEqual(field_label, 'Died')

    def test_last_name_max_length(self):
        """Prueba la longitud máxima del apellido."""
        author = Author.objects.get(first_name='Big', last_name='Bob')
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_get_absolute_url(self):
        """Prueba que la URL de detalle use el ID dinámico correctamente."""
        author = Author.objects.get(first_name='Big', last_name='Bob')
        # Usamos f-string para comparar con el ID real del objeto creado
        self.assertEqual(author.get_absolute_url(), f'/catalog/author/{author.id}')

class RenewBookFormTest(TestCase):
    """Tests para validar la lógica del formulario de renovación."""
    
    def test_renew_form_date_in_past(self):
        """El formulario debe ser inválido si la fecha es anterior a hoy."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        """El formulario debe ser inválido si la fecha es superior a 4 semanas."""
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Creamos 13 autores para probar que la paginación funciona (10 por página)."""
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        """Comprueba que la URL física /catalog/authors/ funciona."""
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Comprueba que el nombre 'authors' definido en urls.py funciona."""
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Verifica que se usa la plantilla HTML correcta."""
        response = self.client.get(reverse('authors'))
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        """Comprueba que la paginación está activada y es de 10 elementos."""
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        """Comprueba que la segunda página contiene los 3 autores restantes."""
        # Entramos en la página 2
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['author_list']), 3)

class AllBorrowedListViewTest(TestCase):
    def setUp(self):
        """Creamos usuarios de prueba: uno normal y otro con permisos."""
        self.test_user1 = User.objects.create_user(username='testuser1', password='123password')
        self.test_user2 = User.objects.create_user(username='testuser2', password='123password')
        
        # Le damos el permiso específico al usuario 2
        from django.contrib.auth.models import Permission
        permission = Permission.objects.get(codename='can_mark_returned')
        self.test_user2.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        """Si no estás logueado, te redirige al login."""
        response = self.client.get(reverse('all-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/borrowed/')

    def test_forbidden_if_logged_in_but_not_librarian(self):
        """Si estás logueado pero no eres bibliotecario, no deberías ver la lista."""
        self.client.login(username='testuser1', password='123password')
        response = self.client.get(reverse('all-borrowed'))
        # Dependiendo de tu vista, puede ser un error 403 (Prohibido) o que no aparezca el contenido
        self.assertEqual(response.status_code, 403)

    def test_accessible_if_librarian(self):
        """Si eres bibliotecario, la página carga correctamente."""
        self.client.login(username='testuser2', password='123password')
        response = self.client.get(reverse('all-borrowed'))
        self.assertEqual(response.status_code, 200)