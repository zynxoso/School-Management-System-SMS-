from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    RELIGION_CHOICES = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Others', 'Others'),
    ]

    # Personal Information
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique Student ID")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True)
    nationality = models.CharField(max_length=50, default='Filipino')
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    # Academic Information
    grade_level = models.IntegerField()
    section = models.CharField(max_length=20)
    admission_date = models.DateField(auto_now_add=True)
    previous_school = models.CharField(max_length=100, blank=True)
    academic_year = models.CharField(max_length=9, help_text="Format: YYYY-YYYY")

    # Contact Information
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17)

    # Parent/Guardian Information
    father_name = models.CharField(max_length=100, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    father_email = models.EmailField(blank=True)

    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    mother_email = models.EmailField(blank=True)

    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_relationship = models.CharField(max_length=50, blank=True)
    guardian_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    guardian_email = models.EmailField(blank=True)

    # Medical Information
    medical_conditions = models.TextField(blank=True, help_text="List any medical conditions")
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)

    # Status and System Fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['grade_level', 'last_name', 'first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
