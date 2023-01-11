from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'
    ROLE_CHOICES = [
        (user, 'User'),
        (moderator, 'Moderator'),
        (admin, 'Admin'),
    ]
    role = models.CharField(
        'Роль пользователя',
        max_length=15,
        choices=ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        default=''
    )
    password = models.CharField(
        'Пароль',
        max_length=255,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_username'
            )
        ]


class Category(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    year = models.IntegerField()
    description = models.TextField(null=False, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.DO_NOTHING
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        'текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
