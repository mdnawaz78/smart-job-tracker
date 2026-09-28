
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Interview", "Interview"),
        ("Rejected", "Rejected"),
        ("Offer", "Offer"),
        ("Accepted", "Accepted"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=100
    )

    job_title = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    application_date = models.DateField()

    deadline = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    job_url = models.URLField(
        blank=True
    )

    salary = models.CharField(
        max_length=50,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def deadline_status(self):
        """
        Returns the current status of the application deadline.
        """

        if not self.deadline:
            return "No deadline"

        today = timezone.localdate()

        days_left = (self.deadline - today).days

        if days_left < 0:
            return "Overdue"

        elif days_left == 0:
            return "Due Today"

        elif days_left <= 3:
            return f"Due in {days_left} days"

        else:
            return f"{days_left} days left"

    def deadline_status_class(self):
        """
        Returns a Bootstrap class based on deadline status.
        """

        if not self.deadline:
            return "secondary"

        today = timezone.localdate()

        days_left = (self.deadline - today).days

        if days_left < 0:
            return "danger"

        elif days_left == 0:
            return "danger"

        elif days_left <= 3:
            return "warning"

        else:
            return "success"

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class ApplicationStatusHistory(models.Model):

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    status = models.CharField(
        max_length=20,
        choices=JobApplication.STATUS_CHOICES
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.job_application.job_title} - {self.status}"

