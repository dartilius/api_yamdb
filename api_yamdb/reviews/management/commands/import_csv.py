from django.core.management.base import BaseCommand

from ._csv_tools import import_from_csv


class Command(BaseCommand):
    """Использование:
    manage.py -p|--path <путь> путь относительно settings.BASE_DIR
    Важна последовательность заполнения БД."""
    help = (
        'Импорт .csv файла(ов) в БД.\n'
        'Использование: -p | --path <путь>'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default=False,
            help='относительный путь к csv'
        )

    def handle(self, *args, **options):
        path = None
        if options['path']:
            path = options['path']
            self.stdout.write(f'Указан путь до csv: {path}')
        else:
            self.stdout.write('Путь до csv не задан')

        import_from_csv(path)
