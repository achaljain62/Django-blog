from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now=timezone.now()
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (  Q(title__icontains= query) |
					Q(content__icontains =query) |
					Q(user__email__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					)
		return self.filter(lookup)


class BlogPostManager(models.Manager):
	def get_query_set(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_query_set().published()

	def search(self, query=None):
		if query is None:
			return self.get_query_set().none()
		return self.get_query_set().published().search(query)


class BlogPost(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ["-updated","-publish_date",  "-timestamp"]

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_update_url(self):
        return f"{self.get_absolute_url()}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


def __str__(self):
    return f"{self.title} - {self.content}"
