from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    passout_year = models.IntegerField()
    skills = models.TextField()
    preferred_job_role = models.CharField(max_length=100)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='announcement_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class JobPosting(models.Model):
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    package = models.CharField(max_length=100)
    apply_link = models.URLField()
    description = models.TextField()
    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='job_images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Call Received', 'Call Received'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Interview Attended', 'Interview Attended'),
        ('Offer Received', 'Offer Received'),
        ('Joined', 'Joined'),
    ]
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Applied'
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.job}"