from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    admission_date = models.DateField(null=True, blank=True)
    current_class = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'user_type': 'parent'})
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.relationship}"
