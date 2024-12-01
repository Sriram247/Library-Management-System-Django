from django.db import models

from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=256)

    def __str__(self):
        return self.uname


class Genre(models.Model):
    gname = models.CharField(max_length=50, primary_key=True)
    gdesc = models.CharField(max_length=256)

    def __str__(self):
        return self.gname


class Publisher(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.pname


class Author(models.Model):
    aid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=50)

    def __str__(self):
        return self.aname


class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    btitle = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.btitle


class Contains(models.Model):
    bid = models.ForeignKey(Book, on_delete=models.CASCADE)
    gname = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('bid', 'gname')

    def __str__(self):
        return f"{self.bid} contains {self.gname}"


class Written(models.Model):
    bid = models.ForeignKey(Book, on_delete=models.CASCADE)
    aid = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('bid', 'aid')

    def __str__(self):
        return f"{self.aid} wrote {self.bid}"


class Published(models.Model):
    bid = models.ForeignKey(Book, on_delete=models.CASCADE)
    pid = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('bid', 'pid')

    def __str__(self):
        return f"{self.bid} published by {self.pid}"
