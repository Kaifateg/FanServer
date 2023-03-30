from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Reply(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class Post(models.Model):
    TYPE = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Traders', 'Торговцы'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potioneers', 'Зельевары'),
        ('Spell masters', 'Мастера заклинаний')
    ]
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=40, choices=TYPE, default='Nobody')
    files = models.FileField(upload_to='files/%Y/%m/%d/', blank=True)
    time_create_post = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
