import datetime
from django.test import TestCase
from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'renewal date'
        )

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        expected_text = (
            'Introduce una fecha entre hoy y 4 semanas (por defecto 3).'
        )
        self.assertEqual(form.fields['renewal_date'].help_text, expected_text)

    def test_renew_form_date_in_past(self):
        """La fecha en el pasado no debe ser válida"""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        """La fecha de hoy debe ser válida"""
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        """La fecha dentro de 4 semanas debe ser válida"""
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        """La fecha más allá de 4 semanas no debe ser válida"""
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
