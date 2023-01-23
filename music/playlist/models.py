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


class Album(models.Model):
    album_name = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    image = models.ImageField(max_length=255, default="avatar.png")
    release_year = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-release_year']


class Song(models.Model):
    artist = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, default="avatar.png")
    mp3 = models.CharField(max_length=255, null=True)
    oga = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['id']


class Collection(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True, null=True)
    purchased = models.BooleanField(default=False)
    albumlist = models.ManyToManyField(Album)
    songlist = models.ManyToManyField(Song)
    title = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_at'] 


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


class Transaction(models.Model):
    status = models.BooleanField(default=False)
    message = models.CharField(max_length=255, blank=True)
    data = models.TextField(null=True, blank=True)

    
class Donate(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class GuestUser(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



