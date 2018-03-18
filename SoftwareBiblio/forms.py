from django import forms


class ImageForm(forms.Form):
    picture = forms.ImageField()
    book_isbn = forms.CharField(max_length=50)
