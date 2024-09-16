from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
class PublishedManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status=Post.Status.PUBLISHED)
        return queryset


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT=('DF','draft')
        PUBLISHED=('PB','published')
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_posts')
    users_like=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='posts_liked',blank=True)
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    text=models.TextField()
    status=models.CharField(max_length=2,choices=Status,default=Status.DRAFT)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager(through=UUIDTaggedItem)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-publish']
        indexes=[models.Index(fields=['-publish'])]


    def get_absolute_url(self):
        return reverse("post_detail", args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,unique=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_comments')
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['created']
        indexes=[
        models.Index(fields=('created',))
        ]

    def __str__(self):
        return f'comment by {self.user.username} on {self.post.title}'

