from django.db import models
from django.contrib.auth.models import User
from jalali_date import date2jalali, datetime2jalali


# Create your models here.
class TodoItem(models.Model):
    work = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.work

    def get_created_jalali(self):
        return date2jalali(self.date)
