from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    username = models.CharField(unique=True, max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.jpg')
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_loggedin = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Collection(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']    


class Album(models.Model):
    album_name = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    albumlist = models.ForeignKey(Collection, related_name='album', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(max_length=255, default="avatar.png")
    release_year = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-release_year']


class Song(models.Model):
    artist = models.CharField(max_length=255, blank=True)
    songlist = models.ManyToManyField(Collection, related_name='songlist')
    title = models.CharField(max_length=255, null=True)
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, default="avatar.png")
    mp3 = models.CharField(max_length=255, null=True)
    oga = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['id']


class downloadLog(models.Model):
    album_name = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, related_name='downloads', on_delete=models.CASCADE, default='')
    artist = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    album_id = models.IntegerField()
    album_img_path = models.CharField(max_length=255, blank=True)
    track_path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField()
    songlist = models.CharField(max_length=255, blank=True)
    meta = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('created_at',)

    





