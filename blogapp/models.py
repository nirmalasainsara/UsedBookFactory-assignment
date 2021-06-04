from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Author(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="author_name")
    articles = models.ManyToManyField(Article)

