from django.db import models
from django.utils import timezone


class Comment(models.Model):
    """
    User's comment
    """
    author = models.ForeignKey("Commenter", on_delete=models.SET_NULL, null=True, related_name="author")
    date_published = models.DateTimeField(default=timezone.now)
    place = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return '@{author}: {text}'.format(author=self.author.name,
                                          text=self.get_short())

    def get_short(self):
        return self.text if len(self.text) <= 10 else self.text[:7] + '...'


class Commenter(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DocumentManager(models.Manager):
    def create_document(self, title, url):
        clean_url = self.clean_url(url)
        site, _ = Site.objects.get_or_create(domain=self.get_domain_from_clean_url(clean_url))
        return self.create(site=site, title=title, url=clean_url)

    def get_domain_from_clean_url(self, clean_url):
        if clean_url.startswith('www.'):
            i1 = len('www.')
        else:
            i1 = 0
        i2 = clean_url.find('/')
        return clean_url[i1:i2]

    def clean_url(self, url):
        if url.startswith('http://'):
            url = url[len('http://'):]
        elif url.startswith('https://'):
            url = url[len('https://'):]
        if url.endswith('/'):
            url = url[:-1]
        return url


class Document(models.Model):
    """
    Web page or document
    """
    objects = DocumentManager()
    site = models.ForeignKey("Site", null=True, related_name="documents")
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=300, unique=True)

    def __str__(self):
        return self.title


    def get_date_active(self):
        comments = self.comments.filter(place=self).order_by('-date_published')
        if comments:
            return comments[0].date_published
        else:
            return None

    def get_date_started(self):
        comments = self.comments.filter(place=self).order_by('date_published')
        if comments:
            return comments[0].date_published
        else:
            return None


class Site(models.Model):
    domain = models.CharField(max_length=50, unique=True)
    uses_ssl = models.BooleanField(default=False)

    def __str__(self):
        return self.domain

class Vote(models.Model):
    comment = models.ForeignKey(Comment, related_name='comment')
    is_in_support = models.BooleanField()
    voter = models.ForeignKey(Commenter)
