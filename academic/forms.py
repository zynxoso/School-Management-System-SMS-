from django import forms
from .models import (
    AcademicYear, Class, Subject, ClassSubject,
    StudentEnrollment, Attendance, Grade
)

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'academic_year', 'class_teacher', 'section', 'capacity']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'credits']

class ClassSubjectForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    day = forms.ChoiceField(choices=DAYS_OF_WEEK, required=True)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    
    class Meta:
        model = ClassSubject
        fields = ['subject', 'teacher']
    
    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if day and start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time")
            
            # Create schedule JSON
            cleaned_data['schedule'] = {
                day: {
                    'start': start_time.strftime('%H:%M'),
                    'end': end_time.strftime('%H:%M')
                }
            }
        return cleaned_data

class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = StudentEnrollment
        fields = ['student', 'status']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            })
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_subject', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_subject', 'assessment_type', 'score', 'max_score', 'date', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'status_{student.id}'] = forms.ChoiceField(
                    choices=Attendance._meta.get_field('status').choices,
                    initial='present',
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
                self.fields[f'remarks_{student.id}'] = forms.CharField(
                    required=False,
                    widget=forms.Textarea(attrs={'rows': 2})
                )

class BulkGradeForm(forms.Form):
    assessment_type = forms.ChoiceField(choices=Grade._meta.get_field('assessment_type').choices)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'score_{student.id}'] = forms.DecimalField(
                    max_digits=5,
                    decimal_places=2,
                    widget=forms.NumberInput(attrs={'step': '0.01'})
                )
                self.fields[f'max_score_{student.id}'] = forms.DecimalField(
                    max_digits=5,
                    decimal_places=2,
                    initial=100.00,
                    widget=forms.NumberInput(attrs={'step': '0.01'})
                )
                self.fields[f'remarks_{student.id}'] = forms.CharField(
                    required=False,
                    widget=forms.Textarea(attrs={'rows': 2})
                )
