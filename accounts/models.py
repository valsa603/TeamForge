from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.user.username


