"""Скрипт наполняющий данные из файлов csv в базу данных.

    Файлы находятся в ../static/data/*.csv
    Запуск:
        python manage.py load_csv       - добавление в БД
        python manage.py load_csv -u
            - добавление в БД. Найденные элементы будут обновлены
        python manage.py load_csv -d
            - Предваритльено удаляются все таблицы, кроме users
        python manage.py load_csv -d
            - Предваритльено удаляются все таблицы, в том числе users
"""
import os
import csv
import logging
from django.core.management.base import BaseCommand, CommandParser

from api_yamdb.settings import BASE_DIR
from reviews.models import CustomUser, Category, Genre, Title, Review, Comment

logger = logging.getLogger(__name__)
# logging.getLogger('asyncio').setLevel(logging.WARNING)


class Command(BaseCommand):
    PATH_CSV = os.path.join(BASE_DIR, 'static', 'data')
    FILES_OF_MODELS = {
        'users.csv': CustomUser,
        'category.csv': Category,
        'genre.csv': Genre,
        'titles.csv': Title,
        'genre_title.csv': Title.genre.through,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-d', '--delete',
            action='store_const', const=True,
            help=('Предварительно удаление всех данных, кроме user.')
        )

        parser.add_argument(
            '-du', '--delete-user',
            action='store_const', const=True,
            help=('Предварительно удаляется все данные в том числе user.')
        )

        parser.add_argument(
            '-u', '--update',
            action='store_const', const=True,
            help=('При нахождении элемента и другим содержаниеи обновляется.')
        )

    def handle(self, *args, **options) -> None:
        update = options.get('update')
        delete = options.get('delete')
        delete_user = options.get('delete_user')
        if delete or delete_user:
            for model in self.FILES_OF_MODELS.values():
                if model == CustomUser and not delete_user:
                    continue
                model.objects.all().delete()
                logger.debug(f'Данные {model.__name__} удалены.')

        data = dict()
        for name_file, model in self.FILES_OF_MODELS.items():
            short_name_file = name_file.replace('.csv', '')
            data[short_name_file] = list()
            full_name_file = os.path.join(self.PATH_CSV, name_file)
            if not os.path.isfile(full_name_file):
                continue
            with open(full_name_file) as file:
                reader = csv.DictReader(file)
                for numb, row in enumerate(reader, start=2):
                    try:
                        data[short_name_file].append(dict(**row))
                    except TypeError:
                        logger.error(f'В {short_name_file} в {numb} строке '
                                     'не подходящие данные')

        # Category
        for category in data['category']:
            slug = category.get('slug')
            fields = ('name',)
            defaults = {key: category.get(key) for key in fields}
            model = Category
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(slug=slug, defaults=defaults)
            category['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # CustomUser
        for user in data['users']:
            username = user.get('username')
            fields = ('email', 'role', 'bio', 'first_name', 'last_name')
            defaults = {key: user.get(key) for key in fields}
            model = CustomUser
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(username=username, defaults=defaults)
            user['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # Genre
        for genre in data['genre']:
            slug = genre.get('slug')
            fields = ('name',)
            defaults = {key: genre.get(key) for key in fields}
            model = Genre
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(slug=slug, defaults=defaults)
            genre['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # Titles
        titles = data['titles']
        for title in titles:
            try:
                category = next((category for category in data['category']
                                 if category['id'] == title['category_id']))
            except StopIteration:
                logger.warning(f'Строка {title["id"]}. "{title["name"]}" '
                               f'({title["year"]}) не удалось найти '
                               f'{title["category_id"]} - номер категории.'
                               'Строка не добавляется в БД.')
                titles.remove(title)
                continue

            name = title.get('name')
            year = title.get('year')
            category_id = category['db_id']
            fields = ()
            defaults = {key: title.get(key) for key in fields}
            model = Title
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(name=name,
                                  year=year,
                                  category_id=category_id,
                                  defaults=defaults)
            title['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # Title.genre.through
        genre_titles = data['genre_title']
        for genre_title in genre_titles:
            try:
                genre = next((genre for genre in data['genre']
                              if genre['id'] == genre_title['genre_id']))
                title = next((title for title in data['titles']
                              if title['id'] == genre_title['title_id']))
            except StopIteration:
                logger.warning(f'Строка {genre_title["id"]} - неверная.'
                               f'{genre_title["genre_id"]} - номер жанра, или '
                               f'{genre_title["title_id"]} - номер названия.'
                               'Строка не добавляется в БД.')
                genre_titles.remove(genre_title)
                continue

            genre_id = genre['db_id']
            title_id = title['db_id']
            fields = ()
            defaults = {key: genre_title.get(key) for key in fields}
            model = Title.genre.through
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(genre_id=genre_id,
                                  title_id=title_id,
                                  defaults=defaults)
            genre_title['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # Review
        reviews = data['review']
        for review in reviews:
            try:
                author = next((author for author in data['users']
                              if author['id'] == review['author_id']))
                title = next((title for title in data['titles']
                              if title['id'] == review['title_id']))
            except StopIteration:
                logger.warning(f'Строка {review["id"]} - неверная.'
                               f'{review["author_id"]} - номер автора, или '
                               f'{review["title_id"]} - номер названия.'
                               'Строка не добавляется в БД.')
                reviews.remove(review)
                continue

            author_id = author['db_id']
            title_id = title['db_id']
            fields = ('text', 'score', 'pub_date')
            defaults = {key: review.get(key) for key in fields}
            model = Review
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(author_id=author_id,
                                  title_id=title_id,
                                  defaults=defaults)
            review['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')

        # Comments
        comments = data['comments']
        for comment in comments:
            try:
                author = next((author for author in data['users']
                              if author['id'] == comment['author_id']))
                title = next((review for review in data['review']
                              if review['id'] == comment['review_id']))
            except StopIteration:
                logger.warning(f'Строка {comment["id"]} - неверная.'
                               f'{review["author_id"]} - номер автора, или '
                               f'{review["review_id"]} - номер обзора. '
                               'Строка не добавляется в БД.')
                reviews.remove(review)
                continue

            author_id = author['db_id']
            review_id = review['db_id']
            fields = ('text', 'pub_date')
            defaults = {key: comment.get(key) for key in fields}
            model = Comment
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(author_id=author_id,
                                  review_id=review_id,
                                  defaults=defaults)
            comment['db_id'] = obj.id
        logger.debug(f'Данные {model.__name__} обработаны.')
