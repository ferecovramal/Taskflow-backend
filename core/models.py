from django.db.models import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=25)
    address = models.TextField()
    def __str__(self):
        return self.name


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete= models.CASCADE, related_name='users', null=True, blank=True)
    is_admin = models.BooleanField(default=False)

class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, default='Pending')
    assigned_users = models.ManyToManyField(User, related_name='tasks')
    organization = models.ForeignKey(Organization,on_delete= models.CASCADE,related_name='tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete= models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.field_name}"