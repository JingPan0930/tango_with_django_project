from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True,blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):  # For Python 2, use __unicode__ too

        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE, )
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)


    def __str__(self):  # For Python 2, use __unicode__ too

        return self.title

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'category', 'url')


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

# =================================================
class PostAd(models.Model):
    title = models.CharField(max_length=128,unique=True)
    image = models.ImageField(upload_to='ad_images/', blank=True)
    description = models.TextField(blank=True)
    price= models.IntegerField(default=0)
    location = models.CharField(max_length=7,default="")
    email = models.EmailField(max_length=30 )
    phone = models.IntegerField(max_length=11, blank=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.email

# ==============
class Comment(models.Model):
    name = models.CharField(max_length=30,unique=True)
    email =models.EmailField(max_length=20)
    phone = models.IntegerField(max_length=11, blank=True)
    message= models.TextField()

    def __str__(self):
        return self.name
