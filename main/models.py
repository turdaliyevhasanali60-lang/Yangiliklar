from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    intro = models.TextField()
    cover = models.ImageField(upload_to='articles/cover')
    read_time = models.DurationField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=255, blank=True, null=True)

    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.CASCADE)

    published = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if self.important:
            Article.objects.exclude(id=self.id).filter(important=True).update(important=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Context(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    article = models.ForeignKey(Article, related_name='context', on_delete=models.CASCADE)

class Comment(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255,blank=True, null=True)
    text = models.TextField()
    published = models.BooleanField(default=False)

    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Newsletter(models.Model):
    email = models.EmailField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Moment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='moments', max_length=1000)

    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)

    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"