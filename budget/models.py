from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.category_name


class Expence(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    notes = models.CharField(max_length=250, null=True)
    amount = models.IntegerField()
    user = models.CharField(max_length=120)
    date = models.DateField()

    def __str__(self):
        return self.user


 #expences = Expence.objects.all()
#>>> date = [exp.date for exp in expences]
#>>> date
