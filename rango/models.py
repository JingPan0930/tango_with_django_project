from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField()
    slug = models.SlugField(unique=True)
    slug = models.SlugField(blank=True)   
    def save(self, *args, **kwargs):  # what does *args, **kwargs do here?
        self.slug = slugify(self.name)
        #  super(Category, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length = 128)
    url = models.URLField(unique = True)
    views = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attribute we wish to include.
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
