import csv

from django.apps import apps
from django.conf import settings
from django.db.models import Avg

BASE_DIR = settings.BASE_DIR

PATH_CSV = '/static/data/'
MODELS_FILES = {
    'User': 'users',
    'Category': 'category',
    'Genre': 'genre',
    'Title': 'titles',
    'Review': 'review',
    'Comment': 'comments',
    'GenreTitle': 'genre_title',
}
CSV_EXT = '.csv'

IMPORT_MATRIX = (
    (
        'User',
        (
            'users',
            {
                'id': 'id',
                'username': 'username',
                'email': 'email',
                'role': 'role',
                'bio': 'bio',
                'first_name': 'first_name',
                'last_name': 'last_name',
            }
        )
    ),
    (
        'Category', (
            'category',
            {
                'id': 'id',
                'name': 'name',
                'slug': 'slug',
            }
        )
    ),
    (
        'Genre',
        (
            'genre',
            {
                'id': 'id',
                'name': 'name',
                'slug': 'slug',
            }
        )
    ),
    (
        'Title',
        (
            'titles',
            {
                'id': 'id',
                'name': 'name',
                'year': 'year',
                'category': 'Category.id',
            }
        )
    ),
    (
        'Review',
        (
            'review',
            {
                'id': 'id',
                'title_id': 'Title.id',
                'text': 'text',
                'author': 'User.id',
                'score': 'score',
                'pub_date': 'pub_date',
            }
        )
    ),
    (
        'Comment',
        (
            'comments',
            {
                'id': 'id',
                'review_id': 'Review.id',
                'text': 'text',
                'author': 'User.id',
                'pub_date': 'pub_date',
            }
        )
    ),
)
TITLE_GENRE_MATRIX = (
    'Title',
    (
        'genre_title',
        {
            'id': 'id',
            'title_id': 'Title.id',
            'genre_id': 'Genre.id'
        }
    )
)

MODEL_LIST = (
    'reviews.Title',
    'reviews.Genre',
    'reviews.Category',
    'reviews.Review',
    'reviews.Comment',
    'users.User',
)
MODEL_LINKS = dict()

for model in MODEL_LIST:
    model_key = model.split('.')[1]
    model_link = apps.get_model(model)
    MODEL_LINKS[model_key] = model_link


def read_csv_file(file_name):
    "Функция для чтения CSV-файла."
    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        return list(file_reader)


def get_file_fields(file_struct):
    "Получения списка полей файла и связанных моделей."
    file_fields = file_struct[0]
    bd_fields = [field.replace('_id', '') for field in file_fields]
    func_fields = []
    for field_name in file_fields:
        bd_name = file_struct[1][field_name]
        if len(bd_name.split('.id')) == 2:
            rel_model_name = bd_name.split('.id')[0]
            rel_model = MODEL_LINKS[rel_model_name]
            func_fields.append(rel_model)
        else:
            func_fields.append(None)
    return file_fields, bd_fields, func_fields


def create_objects(model, model_link, bd_fields, func_fields, line_fields):
    "Cоздание объектов в БД."
    object_fields = dict()
    for e in range(len(line_fields)):
        if func_fields[e]:
            object_fields[bd_fields[e]],
            _ = func_fields[e].objects.get_or_create(pk=line_fields[e])
        else:
            object_fields[bd_fields[e]] = line_fields[e]
    try:
        model_link.objects.create(**object_fields)
        return True
    except Exception as e:
        print(f'Ошибка создания записи: {e}')
        return False


def import_from_csv(path_csv=None, models_files=None, matrix=None):
    "Основная функция импорта данных из CSV-файлов."
    if path_csv is None:
        path_csv = PATH_CSV
    if models_files is None:
        models_files = MODELS_FILES
    if matrix is None:
        matrix = IMPORT_MATRIX

    for model_file in matrix:
        model, file_struct = model_file
        file_name = ''.join((BASE_DIR, path_csv, file_struct[0], CSV_EXT))
        print('\n\nВзят в работу файл: ', file_name)

        file_data = read_csv_file(file_name)
        count = len(file_data)
        obj_count = 0

        file_fields, bd_fields, func_fields = get_file_fields(file_struct)

        for i in range(1, count):
            line_fields = file_data[i]
            if create_objects(model, MODEL_LINKS[model], bd_fields,
                              func_fields, line_fields):
                obj_count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # Если вариант БД с полем "rating" в "Title"
    title_model = MODEL_LINKS['Title']
    if hasattr(title_model, 'rating'):
        for title in title_model.objects.all():
            if title.reviews.all():
                rating_obj = title.reviews.aggregate(Avg('score'))
                title.rating = round(rating_obj['score__avg'])
                title.save()


def export_to_csv():
    pass
