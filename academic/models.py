from django.db import models
from accounts.models import User

class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'teacher'})
    section = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.section} ({self.academic_year})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"

class ClassSubject(models.Model):
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    schedule = models.TextField()  # Store schedule as JSON string

    class Meta:
        unique_together = ('class_group', 'subject')

    def __str__(self):
        return f"{self.subject} - {self.class_group}"

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('transferred', 'Transferred'),
    ])

    class Meta:
        unique_together = ('student', 'class_group')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_group}"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ])
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'class_subject', 'date')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_subject} - {self.date}"

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=50, choices=[
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('mid_term', 'Mid Term'),
        ('final', 'Final'),
    ])
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_subject} - {self.assessment_type}"

    @property
    def percentage(self):
        return (self.score / self.max_score) * 100
