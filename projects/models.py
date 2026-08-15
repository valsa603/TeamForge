from django.db import models
from django.contrib.auth.models import User
from accounts.models import Skill


class Project(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_projects"
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    required_skills = models.ManyToManyField(
        Skill,
        blank=True
    )

    team_size = models.PositiveIntegerField(default=2)

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning"
    )

    members = models.ManyToManyField(
        User,
        blank=True,
        related_name="joined_projects"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Invitation(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )

    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.inviter.username} → "
            f"{self.invitee.username} "
            f"({self.project.title})"
        )


class Task(models.Model):

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("progress", "In Progress"),
        ("completed", "Completed"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo"
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

class Notification(models.Model):

     recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

     message = models.CharField(
        max_length=255
    )

     is_read = models.BooleanField(
        default=False
    )

     created_at = models.DateTimeField(
        auto_now_add=True
    )

     def __str__(self):
        return f"{self.recipient.username} - {self.message}"