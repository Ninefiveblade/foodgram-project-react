# Продуктовый помощник

![example workflow](https://github.com/Ninefiveblade/foodgram-project-react/actions/workflows/main.yml/badge.svg)

#### Тут можно создавать рецепты, качать список покупок и держать все свои любимые рецепты под рукой. Подписывайся на авторов, чьи рецепты понравились, добавляй их в избранное, а потом из них выбирай, что хочешь приготовить и добавляй рецепты в список покупок, чтобы не ошибиться в грамовках и ингридиентах, купив только то, что необходимо. Ресторанная еда теперь и дома.

#### Автор: Иван, Яндекс Практикум.
#### Технологии: React, Django REST, Docker, Djoser, Python 3.9, 

## Установить проект:

```git clone git@github.com:Ninefiveblade/foodgram-project-react.git```

## Наполнение .env path (your_path/infra/.env)

```
ALLOWED_HOSTS = "Your hosts"
SECRET_KEY = "Your secret key"
ENTER_PASS = "Your email Email SMTP PASS"

AUTH_USER_MODEL="your user model"
LOGIN_FIELD="login field"
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD= "your passeord"
DB_HOST="your container name"
DB_PORT=5432 
```
## Запустить демо можно по адресу:

```http://foodfound.myvnc.com/recipes```

## Запустить проект:

```your_path/infra/docker-compose up -d```

## Выполнить миграции:

```docker-compose exec backend python manage.py makemigrations```
```docker-compose exec backend python manage.py migrate```

## Создать суперпользователя:

```docker-compose exec backend python manage.py createsuperuser```

## Собрать статику для корректного отображения страниц:

```docker-compose exec backend python manage.py collectstatic --no-input```

## Заполнить базу данных:

```docker-compose exec backend python manage.py update```

## Документация:

```http://foodfound.myvnc.com/api/docs/```

## Пример запроса:
#### Получить все рецепты:

```http://foodfound.myvnc.com/recipes```

## Зарегистрироваться:

```http://foodfound.myvnc.com/signup```

## Войти:
```http://foodfound.myvnc.com/signin```

## Сохранить дамп базы данных:

```docker-compose exec backend python manage.py dumpdata > fixtures.json```

## License

[LICENSE MIT](LICENSE.md)
