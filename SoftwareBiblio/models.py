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


class BookCover(Image):
    class Meta:
        db_table = "book_cover"


class UnregisteredUser(models.Model):
    email = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'unregistered_user'


class RegisteredUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=20)
    enabled = forms.BooleanField(initial=True)
    address = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    profile_picture = models.OneToOneField(ProfilePicture, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'registered_user'


class Administrator(RegisteredUser):
    class Meta:
        db_table = 'administrator'


class Genre(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'genre'


class Serie(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'serie'


class Author(models.Model):
    normalized_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=60)
    nickname = models.CharField(max_length=20)

    class Meta:
        db_table = 'author'


class Book(models.Model):
    title = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20)
    ISSN = models.CharField(max_length=20)
    series = models.ForeignKey(Serie, on_delete=models.SET_NULL, null=True)
    year = models.IntegerField()
    signature = models.CharField(max_length=50)
    publisher = models.CharField(max_length=40)
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)
    cover = models.OneToOneField(BookCover, on_delete=models.SET_NULL, null=True)
    cover_type = models.CharField(max_length=50)  # hardcover, etc
    edition = models.CharField(max_length=50)
    physical_description = models.CharField(max_length=100)

    class Meta:
        db_table = 'book'


class Review(models.Model):
    text = models.CharField(max_length=1000)
    reviewer = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'


class Loan(models.Model):
    loan_date = models.DateTimeField()
    return_date = models.DateTimeField()
    fee_time = models.DateTimeField()
    fee = models.FloatField()
    admin = models.ForeignKey(Administrator, on_delete=models.SET_NULL, null=True, related_name='admin')
    fee_per_book = models.FloatField()
    reader = models.ForeignKey(RegisteredUser, on_delete=models.SET_NULL, null=True, related_name='reader')

    class Meta:
        db_table = 'loan'


class Copy(models.Model):
    copy_number = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'copy'
