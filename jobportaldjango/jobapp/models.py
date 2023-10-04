from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
@property
def is_verified_display(self):
        return "Verified ✅" if self.is_verified else "Not Verified ❌"
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    def __str__ (self):
        return self.user.username
 
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    image = models.ImageField(upload_to="")
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField()
    schedule = models.CharField(max_length=100,default=False)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__ (self):
        return self.title
 
class Application(models.Model):
    APPLIED = 'applied'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    VIEWED = 'viewed'
    PROFILE_VISITED = 'profile_visited'

    APPLICATION_STATUS_CHOICES = [
        (APPLIED, 'Applied'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (VIEWED, 'Viewed'),
        (PROFILE_VISITED, 'Profile Visited'),
    ]
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)   
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES,default="")
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    resume = models.ImageField(upload_to="")
    apply_date = models.DateField()
    
 
    def __str__ (self):
        return str(self.applicant)
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, blank=True, null=True)
    NOTIFICATION_TYPES = (
        ('applicant_details', 'Applicant Details'),
        ('job_scheduling', 'Job Scheduling'),
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES,default=False)   
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"
    def __str__(self):
        return self.message    
class JobPosting(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_approved = models.BooleanField(default=False) 
