![example workflow](https://github.com/Alyona-safonova/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# **YaMDb Project**

### _СI и CD проекта API YaMDb_

# Описание
API YaMDb собирает отзывы пользователей на различные произведения такие как
фильмы, книги и музыка. Для приложения настроен Continuous Integration (CI) и
Continuous Deployment (CD).

Реализован:
* автоматический запуск тестов;
* обновление образов на DockerHub;
* автоматический деплой на боевой сервер при push-е в главную ветку main.

# Функционал API:
1) Просмотр произведений (кино, музыка, книги), которые подразделяются по жанрам и категориям..
2) Возможность оставлять отзывы на произведения и ставить им оценки, на основе которых построена система рейтингов.
3) Комментирование оставленных отзывов.

Проект разработан командой из трех человек с использованием Git в рамках учебного курса Яндекс.Практикум.
[Ссылка на репозиторий, в котором велась разработка проекта в команде] (https://github.com/Alyona-safonova/api-yamdb)

# Технологии

- [Python 3.8.8](https://www.python.org/downloads/release/python-388/)
- [Django 2.2.16](https://www.djangoproject.com/download/)
- [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
- [PostgreSQL 13.0](https://www.postgresql.org/download/)
- [gunicorn 20.0.4](https://pypi.org/project/gunicorn/)
- [nginx 1.21.3](https://nginx.org/ru/download.html)

# Контейнер
- [Docker 20.10.14](https://www.docker.com/)
- [Docker Compose 2.4.1](https://docs.docker.com/compose/)

# Документация

Для просмотра документации к API перейдите по адресу:
http://158.160.1.225/redoc/

# Установка

Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone https://github.com/Alyona-safonova/yamdb_final.git && cd yamdb_final
```
Перейдите в директорию с файлом _docker-compose.yaml_ и запустите контейнеры:
```sh
cd infra && docker-compose up -d --build
```
После успешного запуска контейнеров выполните миграции в проекте:
```sh
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```sh
docker-compose exec web python manage.py createsuperuser
```
Соберите статику:
```sh
docker-compose exec web python manage.py collectstatic --no-input
```
Создайте дамп (резервную копию) базы данных:
```sh
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```sh
docker-compose down -v
```
## Автор:
[Сафонова Алена](https://github.com/Alyona-safonova)
