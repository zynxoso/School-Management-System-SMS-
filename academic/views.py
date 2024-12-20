from django.views.generic import (
    ListView, DetailView, View, CreateView,
    UpdateView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from accounts.models import User
from accounts.decorators import role_required
from django import forms
from .forms import ClassSubjectForm, StudentEnrollmentForm
from .models import (
    AcademicYear, Class, Subject, ClassSubject, StudentEnrollment,
    Attendance, Grade
)

import json

# Mixins
class RoleRequiredMixin:
    role_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.role_required and request.user.user_type != self.role_required and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# Class Management Views
class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'academic/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(academic_year__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.user_type == 'admin':
            context['form'] = ClassCreateView.as_view()(self.request).context_data['form']
        return context

class ClassCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Class
    template_name = 'academic/class_form.html'
    fields = ['name', 'section', 'class_teacher', 'capacity']
    success_url = reverse_lazy('academic:class_list')
    role_required = 'admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if not active_year:
            context['error_message'] = "No active academic year found. Please create and activate an academic year first."
        return context

    def form_valid(self, form):
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if not active_year:
            form.add_error(None, "No active academic year found. Please create and activate an academic year first.")
            return self.form_invalid(form)
        form.instance.academic_year = active_year
        return super().form_valid(form)

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'academic/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.object
        
        # Get subjects for this class
        context['subjects'] = ClassSubject.objects.filter(class_group=class_obj)
        
        # Get enrolled students
        context['enrolled_students'] = StudentEnrollment.objects.filter(
            class_group=class_obj
        ).select_related('student').order_by('student__first_name', 'student__last_name')
        
        # Get available students (not enrolled in this class)
        enrolled_students = StudentEnrollment.objects.filter(
            class_group=class_obj
        ).values_list('student_id', flat=True)
        
        available_students = User.objects.filter(
            user_type='student'
        ).exclude(
            id__in=enrolled_students
        ).order_by('first_name', 'last_name')
        
        # Create forms with available students
        context['subject_form'] = ClassSubjectForm()
        context['enrollment_form'] = StudentEnrollmentForm()
        context['enrollment_form'].fields['student'].queryset = available_students
        
        context['today'] = timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        class_obj = self.object
        print(f"POST data: {request.POST}")  # Debug print
        
        # Handle student enrollment
        if request.POST.get('action') == 'add_student':
            form = StudentEnrollmentForm(request.POST)
            if form.is_valid():
                enrollment = form.save(commit=False)
                enrollment.class_group = class_obj
                enrollment.save()
                messages.success(request, f'Student {enrollment.student.get_full_name()} has been enrolled.')
            else:
                messages.error(request, 'Failed to enroll student. Please check the form.')
        
        # Handle subject addition
        elif request.POST.get('action') == 'add_subject':
            form = ClassSubjectForm(request.POST)
            if form.is_valid():
                subject = form.save(commit=False)
                subject.class_group = class_obj
                subject.schedule = form.cleaned_data['schedule']  # Get schedule from form cleaning
                try:
                    subject.save()
                    messages.success(request, f'Subject {subject.subject.name} has been added to {class_obj.name} on {form.cleaned_data["day"].title()}s at {form.cleaned_data["start_time"].strftime("%I:%M %p")}')
                except Exception as e:
                    messages.error(request, f'Failed to add subject: {str(e)}')
            else:
                messages.error(request, f'Failed to add subject. Please check the form. Errors: {form.errors}')
        
        return redirect('academic:class_detail', pk=class_obj.pk)

class ClassUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Class
    template_name = 'academic/class_form.html'
    fields = ['name', 'section', 'class_teacher', 'capacity']
    success_url = reverse_lazy('academic:class_list')
    role_required = 'admin'

class ClassSubjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = ClassSubject
    template_name = 'academic/class_subject_form.html'
    fields = ['teacher', 'schedule']
    role_required = 'admin'

    def get_success_url(self):
        return reverse('academic:subject_detail', kwargs={'pk': self.object.subject.pk})

# Subject Management Views
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academic/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Subject
    template_name = 'academic/subject_form.html'
    fields = ['name', 'code', 'description', 'credits']
    success_url = reverse_lazy('academic:subject_list')
    role_required = 'admin'

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'academic/subject_detail.html'
    context_object_name = 'subject'

class SubjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Subject
    template_name = 'academic/subject_form.html'
    fields = ['name', 'code', 'description', 'credits']
    success_url = reverse_lazy('academic:subject_list')
    role_required = 'admin'

# Teacher Views
@method_decorator(role_required('teacher'), name='dispatch')
class TeacherClassListView(LoginRequiredMixin, ListView):
    model = ClassSubject
    template_name = 'academic/teacher_classes.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return ClassSubject.objects.filter(teacher=self.request.user)

@method_decorator(role_required('teacher'), name='dispatch')
class TeacherAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/teacher_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get classes where user is either class teacher or subject teacher
        class_subjects = ClassSubject.objects.filter(teacher=self.request.user)
        class_teacher_of = Class.objects.filter(class_teacher=self.request.user)
        
        # Combine both querysets
        context['class_subjects'] = class_subjects
        context['class_teacher_of'] = class_teacher_of
        context['today'] = timezone.now().date()
        return context

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(role_required('teacher'), name='dispatch')
class AttendanceAPIView(LoginRequiredMixin, View):
    def get(self, request, class_subject_id, date):
        try:
            class_subject = ClassSubject.objects.get(id=class_subject_id, teacher=request.user)
            students = StudentEnrollment.objects.filter(class_group=class_subject.class_group)
            
            # Get existing attendance records
            attendance_records = Attendance.objects.filter(
                class_subject=class_subject,
                date=date
            ).values('student_id', 'status', 'remarks')
            
            attendance_dict = {str(a['student_id']): {'status': a['status'], 'remarks': a['remarks']} 
                             for a in attendance_records}
            
            student_data = []
            for enrollment in students:
                student = enrollment.student
                attendance = attendance_dict.get(str(student.id), {'status': 'present', 'remarks': ''})
                student_data.append({
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'status': attendance['status'],
                    'remarks': attendance['remarks']
                })
            
            return JsonResponse({'students': student_data})
            
        except ClassSubject.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, class_subject_id, date):
        try:
            data = json.loads(request.body)
            class_subject = ClassSubject.objects.get(id=class_subject_id, teacher=request.user)
            
            # Process attendance data
            for student_data in data:
                student_id = student_data['student_id']
                status = student_data['status']
                remarks = student_data.get('remarks', '')
                
                # Update or create attendance record
                Attendance.objects.update_or_create(
                    class_subject=class_subject,
                    student_id=student_id,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': remarks
                    }
                )
            
            return JsonResponse({'success': True, 'message': 'Attendance saved successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ClassSubject.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(role_required('teacher'), name='dispatch')
class TeacherGradesView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/teacher_grades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassSubject.objects.filter(teacher=self.request.user)
        return context

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(role_required('teacher'), name='dispatch')
class GradesAPIView(LoginRequiredMixin, View):
    def get(self, request, class_id, assessment_type):
        try:
            class_subject = ClassSubject.objects.get(id=class_id, teacher=request.user)
            students = StudentEnrollment.objects.filter(class_group=class_subject.class_group)
            
            # Get existing grades
            grades = Grade.objects.filter(
                class_subject=class_subject,
                assessment_type=assessment_type
            ).values('student_id', 'score', 'max_score', 'remarks')
            
            grades_dict = {str(g['student_id']): {
                'score': float(g['score']) if g['score'] else None,
                'max_score': float(g['max_score']) if g['max_score'] else None,
                'remarks': g['remarks']
            } for g in grades}
            
            student_data = []
            for enrollment in students:
                student = enrollment.student
                grade = grades_dict.get(str(student.id), {
                    'score': None,
                    'max_score': None,
                    'remarks': ''
                })
                student_data.append({
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'score': grade['score'],
                    'max_score': grade['max_score'],
                    'remarks': grade['remarks']
                })
            
            return JsonResponse({'students': student_data})
            
        except ClassSubject.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, class_id, assessment_type):
        try:
            data = json.loads(request.body)
            class_subject = ClassSubject.objects.get(id=class_id, teacher=request.user)
            
            # Process each student's grades
            for key, value in data.items():
                if key.startswith('score_'):
                    student_id = key.split('_')[1]
                    score = float(value) if value else None
                    max_score = float(data.get(f'max_score_{student_id}', 0)) if data.get(f'max_score_{student_id}') else None
                    remarks = data.get(f'remarks_{student_id}', '')
                    
                    if score is not None and max_score is not None:
                        # Update or create grade record
                        Grade.objects.update_or_create(
                            class_subject=class_subject,
                            student_id=student_id,
                            assessment_type=assessment_type,
                            defaults={
                                'score': score,
                                'max_score': max_score,
                                'remarks': remarks,
                                'date': timezone.now().date()
                            }
                        )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(role_required('teacher'), name='dispatch')
class TeacherAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/attendance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_subject_id = self.kwargs['class_subject_id']
        date = self.kwargs['date']
        print(f"Class Subject ID: {class_subject_id}, Date: {date}")  # Debugging output
        print(f"URL Parameters: {self.kwargs}")  # Debugging output
        
        # Get the class subject and verify teacher has access
        class_subject = get_object_or_404(ClassSubject, id=class_subject_id)
        if class_subject.teacher != self.request.user:
            raise PermissionDenied
        
        # Get all students enrolled in this class
        enrolled_students = StudentEnrollment.objects.filter(
            class_group=class_subject.class_group,
            status='active'
        ).select_related('student')
        
        # Get existing attendance records for this date
        attendance_records = {
            att.student_id: att 
            for att in Attendance.objects.filter(
                class_subject=class_subject,
                date=date
            )
        }
        
        # Prepare enrollment list with attendance status
        enrollments = []
        for enrollment in enrolled_students:
            attendance = attendance_records.get(enrollment.student.id)
            enrollment.attendance = attendance
            enrollments.append(enrollment)
        
        context.update({
            'class_subject': class_subject,
            'date': date,
            'enrollments': enrollments
        })
        return context

    def post(self, request, *args, **kwargs):
        class_subject_id = self.kwargs['class_subject_id']
        date = self.kwargs['date']
        
        # Get the class subject and verify teacher has access
        class_subject = get_object_or_404(ClassSubject, id=class_subject_id)
        if class_subject.teacher != self.request.user:
            raise PermissionDenied
        
        # Get enrolled students
        enrolled_students = StudentEnrollment.objects.filter(
            class_group=class_subject.class_group,
            status='active'
        ).select_related('student')
        
        # Process attendance for each student
        attendance_data = json.loads(request.body)
        for student_data in attendance_data:
            student_id = student_data['student_id']
            status = student_data['status']
            remarks = student_data['remarks']
            
            # Update or create attendance record
            Attendance.objects.update_or_create(
                student_id=student_id,
                class_subject=class_subject,
                date=date,
                defaults={
                    'status': status,
                    'remarks': remarks
                }
            )
        
        return JsonResponse({'success': True, 'message': 'Attendance saved successfully'})

# Student Views
@method_decorator(role_required('student'), name='dispatch')
class StudentClassListView(LoginRequiredMixin, ListView):
    template_name = 'academic/student_classes.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return StudentEnrollment.objects.filter(
            student=self.request.user,
            status='active'
        )

@method_decorator(role_required('student'), name='dispatch')
class StudentAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/student_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        selected_month = self.request.GET.get('month', '')
        
        # Base queryset
        attendance_records = Attendance.objects.filter(student=self.request.user)
        
        # Apply month filter if selected
        if selected_month:
            attendance_records = attendance_records.filter(date__month=selected_month)
        
        # Calculate attendance statistics
        total = attendance_records.count()
        present = attendance_records.filter(status='present').count()
        absent = attendance_records.filter(status='absent').count()
        late = attendance_records.filter(status='late').count()
        excused = attendance_records.filter(status='excused').count()
        
        # Calculate attendance rate with weighted late attendance
        effective_present = present + (late * 0.5)  # Count late as half present
        countable_total = total - excused  # Don't count excused absences in total
        attendance_rate = round((effective_present / countable_total * 100), 1) if countable_total > 0 else 100
        
        # Calculate monthly data for charts
        monthly_data = {}
        for record in attendance_records:
            month = record.date.month
            if month not in monthly_data:
                monthly_data[month] = {'present': 0, 'absent': 0, 'late': 0, 'excused': 0}
            monthly_data[month][record.status] += 1

        # Calculate subject-wise data for charts with weighted late attendance
        subject_data = {}
        for record in attendance_records:
            subject = record.class_subject.subject.name
            if subject not in subject_data:
                subject_data[subject] = {'total': 0, 'effective_present': 0}
            
            if record.status != 'excused':
                subject_data[subject]['total'] += 1
                if record.status == 'present':
                    subject_data[subject]['effective_present'] += 1
                elif record.status == 'late':
                    subject_data[subject]['effective_present'] += 0.5

        # Calculate subject attendance rates
        subject_attendance_rates = {}
        for subject, data in subject_data.items():
            if data['total'] > 0:
                rate = (data['effective_present'] / data['total']) * 100
                subject_attendance_rates[subject] = round(rate, 1)

        # Convert subject data to lists for the chart
        subject_labels = list(subject_attendance_rates.keys())
        subject_rates = list(subject_attendance_rates.values())

        # Convert monthly chart data
        monthly_present = [0] * 12
        monthly_absent = [0] * 12
        monthly_late = [0] * 12
        monthly_excused = [0] * 12
        
        for month, data in monthly_data.items():
            monthly_present[month-1] = data['present']
            monthly_absent[month-1] = data['absent']
            monthly_late[month-1] = data['late']
            monthly_excused[month-1] = data['excused']

        context.update({
            'attendance': attendance_records.order_by('-date'),
            'selected_month': selected_month,
            'present_count': present,
            'absent_count': absent,
            'late_count': late,
            'excused_count': excused,
            'attendance_rate': attendance_rate,
            'total_classes': total,
            'monthly_present': monthly_present,
            'monthly_absent': monthly_absent,
            'monthly_late': monthly_late,
            'monthly_excused': monthly_excused,
            'subject_labels': subject_labels,
            'subject_rates': subject_rates
        })
        return context

@method_decorator(role_required('student'), name='dispatch')
class StudentGradesView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/student_grades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grades = Grade.objects.filter(student=self.request.user)

        # Calculate GPA and other statistics
        total_score = 0
        total_max = 0
        highest_grade = 0
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

        # Create grade objects with percentage
        grades_with_percentage = []
        for grade in grades:
            percentage = (grade.score / grade.max_score) * 100
            grade_data = {
                'grade': grade,
                'percentage': percentage,
                'letter_grade': self.get_letter_grade(percentage)
            }
            grades_with_percentage.append(grade_data)
            
            total_score += grade.score
            total_max += grade.max_score
            highest_grade = max(highest_grade, percentage)

            # Update grade distribution
            if percentage >= 90:
                grade_distribution['A'] += 1
            elif percentage >= 80:
                grade_distribution['B'] += 1
            elif percentage >= 70:
                grade_distribution['C'] += 1
            elif percentage >= 60:
                grade_distribution['D'] += 1
            else:
                grade_distribution['F'] += 1

        # Calculate overall GPA
        overall_percentage = (total_score / total_max * 100) if total_max > 0 else 0
        
        context.update({
            'grades': grades_with_percentage,
            'overall_percentage': overall_percentage,
            'highest_grade': highest_grade,
            'grade_distribution': grade_distribution,
            'total_grades': len(grades),
        })
        return context

    def get_letter_grade(self, percentage):
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'

# Parent Views
@method_decorator(role_required('parent'), name='dispatch')
class ChildrenListView(LoginRequiredMixin, ListView):
    template_name = 'academic/children_list.html'
    context_object_name = 'children'

    def get_queryset(self):
        return User.objects.filter(
            studentprofile__parent=self.request.user,
            user_type='student'
        )

@method_decorator(role_required('parent'), name='dispatch')
class ChildrenAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/children_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        children = User.objects.filter(
            studentprofile__parent=self.request.user,
            user_type='student'
        )
        context['children_attendance'] = {
            child: Attendance.objects.filter(student=child)
            for child in children
        }
        return context

@method_decorator(role_required('parent'), name='dispatch')
class ChildrenGradesView(LoginRequiredMixin, TemplateView):
    template_name = 'academic/children_grades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        children = User.objects.filter(
            studentprofile__parent=self.request.user,
            user_type='student'
        )
        context['children_grades'] = {
            child: Grade.objects.filter(student=child)
            for child in children
        }
        return context
