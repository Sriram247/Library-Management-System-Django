from django import forms
from .models import *

class AddBookForm(forms.ModelForm):
    GenreIDs = forms.ModelMultipleChoiceField(
        queryset=Book_Genres.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Genres"
    )

    class Meta:
        model = Book_List
        fields = ['BookTitle', 'isbn', 'UserID', 'AuthorID', 'GenreIDs']
