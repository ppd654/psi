from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        # Comprobamos si el usuario 'alumnodb' ya existe
        if not User.objects.filter(username='alumnodb').exists():
            # Si no existe, lo creamos con la contraseña del enunciado
            User.objects.create_superuser(
                'alumnodb', 'alumnodb@test.com', 'alumnodb'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuario "alumnodb" creado con éxito')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('El superusuario "alumnodb" ya existe')
            )
