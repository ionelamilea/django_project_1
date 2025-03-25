from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    page_count = models.IntegerField()

    def __str__(self):
        return "{} by {}, {} pages.".format(self.title, self.author, self.page_count)


class Pizza(models.Model):
    name = models.CharField(max_length=255)
    pizza_type = models.CharField(max_length=255)
    weight = models.IntegerField()
    size = models.IntegerField()

    def __str__(self):
        return "{} este o {} pizza, cu gramajul {} gr si marimea de {} cm.".format(self.name, self.pizza_type, self.weight, self.size)
