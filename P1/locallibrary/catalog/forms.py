import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    # Definimos el campo de fecha con una etiqueta y un texto de ayuda
    renewal_date = forms.DateField(
        help_text="Introduce una fecha entre hoy y 4 semanas (por defecto 3)."
    )

    # Esta es la parte de VALIDACIÓN:
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Comprobar que la fecha no sea en el pasado
        if data < datetime.date.today():
            raise ValidationError(
                _('Fecha de renovación inválida - fecha en el pasado')
            )

        # Comprobar que la fecha no sea más de 4 semanas en el futuro
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Fecha de renovación inválida - más de 4 semanas de plazo')
            )

        # Siempre devuelve los datos limpios
        return data
