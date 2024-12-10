from django.db import models


from django.db import models

class ChangeLog(models.Model):
    table_name = models.CharField(max_length=100)  # Table name where change occurred
    change_type = models.CharField(max_length=50)  # e.g., "Created", "Updated", "Deleted"
    description = models.TextField()  # Details about the change
    timestamp = models.DateTimeField(auto_now_add=True)  # When the change occurred

    def __str__(self):
        return f"{self.change_type} on {self.table_name} at {self.timestamp}"


class list_of_registered_users(models.Model):
    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=256,unique=True)

    def __str__(self):
        return self.UserName


class Book_Genres(models.Model):
    GenreID = models.AutoField(primary_key=True)
    GenreName = models.CharField(max_length=50,unique=True)
    gdesc = models.CharField(max_length=256)

    def __str__(self):
        return self.GenreName


class Book_Publishers(models.Model):
    PublisherID = models.AutoField(primary_key=True)
    PublisherName = models.CharField(max_length=50,unique=True)
    Country = models.CharField(max_length=50)

    def __str__(self):
        return self.PublisherName


class Book_Authors(models.Model):
    AuthorID = models.AutoField(primary_key=True)
    AuthorName = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.AuthorName


class Book_List(models.Model):
    BookID = models.AutoField(primary_key=True)
    BookTitle = models.CharField(max_length=50, unique=True)
    isbn = models.CharField(max_length=20)
    UserID = models.ForeignKey(list_of_registered_users, on_delete=models.CASCADE, null=True, blank=True)
    AuthorID = models.ForeignKey(Book_Authors, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.BookTitle


class Book_and_Genres(models.Model):
    BookID = models.ForeignKey(Book_List, on_delete=models.CASCADE)
    GenreName = models.ForeignKey(Book_Genres, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('BookID', 'GenreName')

    def __str__(self):
        return f"{self.BookID} is from the genre {self.GenreName}"


class Book_and_Authors(models.Model):
    BookID = models.ForeignKey(Book_List, on_delete=models.CASCADE)
    AuthorID = models.ForeignKey(Book_Authors, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('BookID', 'AuthorID')

    def __str__(self):
        return f"{self.AuthorID} wrote {self.BookID}"


class Book_and_Publishers(models.Model):
    BookID = models.ForeignKey(Book_List, on_delete=models.CASCADE)
    PublisherID = models.ForeignKey(Book_Publishers, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('BookID', 'PublisherID')

    def __str__(self):
        return f"{self.BookID} published by {self.PublisherID}"
