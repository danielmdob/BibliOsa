from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='documents/', blank=True)

    class Meta:
        db_table = "image"


class ProfilePicture(Image):
    class Meta:
        db_table = "profile_picture"


class UnregisteredUser(models.Model):
    email = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'unregistered_user'


class RegisteredUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=255, null=True, unique=True)
    card_number = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        db_table = 'registered_user'


class Administrator(RegisteredUser):
    class Meta:
        db_table = 'administrator'


class Genre(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'genre'


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'publisher'


class Serie(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'serie'


class Author(models.Model):
    full_name = models.CharField(max_length=60)

    class Meta:
        db_table = 'author'


class Book(models.Model):
    title = models.CharField(max_length=250)
    isbn10 = models.CharField(max_length=20, null=True)
    isbn13 = models.CharField(max_length=20, null=True)
    issn = models.CharField(max_length=20, null=True)
    call_number = models.CharField(max_length=20, null=True)
    year = models.IntegerField(null=True)
    publisher = models.CharField(max_length=40, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(Author)
    cover = models.URLField(max_length=350)
    edition = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    copies = models.IntegerField()

    class Meta:
        db_table = 'book'


class Review(models.Model):
    text = models.CharField(max_length=1000)
    reviewer = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'


class Loan(models.Model):
    loan_date = models.DateTimeField(auto_now_add=True, null=True)
    return_date = models.DateTimeField()
    reader = models.ForeignKey(RegisteredUser, on_delete=models.SET_NULL, null=True, related_name='reader')
    is_active = models.BooleanField(default=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = 'loan'


class Copy(models.Model):
    copy_number = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'copy'
