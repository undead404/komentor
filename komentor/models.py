from django.db import models
from django.utils import timezone


class Comment(models.Model):
    author = models.CharField(default='guest', max_length=200)
    date_published = models.DateTimeField(default=timezone.now)
    place = models.ForeignKey('Document', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return '@{author}: {text}'.format(author=self.author,
                                          text=self.text if len(self.text) <= 10 else self.text[:7] + '...')


class Document(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=300, unique=True)

    def __str__(self):
        return self.title

    @staticmethod
    def clean_url(url):
        if url.startswith('http://'):
            url = url[len('http://'):]
        elif url.startswith('https://'):
            url = url[len('https://'):]
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get_date_active(self):
        comments = Comment.objects.filter(place=self).order_by('-date_published')
        if comments:
            return comments[0].date_published
        else:
            return None

    def get_date_started(self):
        comments = Comment.objects.filter(place=self).order_by('date_published')
        if comments:
            return comments[0].date_published
        else:
            return None
