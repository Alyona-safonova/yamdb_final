from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import max_value_current_year


class Category(models.Model):
    name = models.CharField('Текст категории', max_length=255)
    slug = models.SlugField('Slug категории', max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField('Текст жанра', max_length=255)
    slug = models.SlugField('Slug жанра', max_length=50, unique=True)


class Title_Genre(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)


class Title(models.Model):
    name = models.CharField('Имя произведения', max_length=255)
    year = models.IntegerField('Год выпуска', validators=[
        max_value_current_year])
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(Genre, through=Title_Genre,
                                   related_name='genre',)
    category = models.ForeignKey(Category, on_delete=models.SET(''),
                                 related_name='category')


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому относится отзыв'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Текст',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name="Оценка",
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Комментарий',
        help_text='Введите ваш комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария')

    class Meta:
        ordering = ('-pub_date',)
