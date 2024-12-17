from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # Class Management
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('class/add/', views.ClassCreateView.as_view(), name='class_create'),
    path('class/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('class/<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_update'),
    
    # Subject Management
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/add/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_update'),
    
    # Teacher Views
    path('teacher/classes/', views.TeacherClassListView.as_view(), name='teacher_classes'),
    path('teacher/attendance/', views.TeacherAttendanceView.as_view(), name='teacher_attendance'),
    path('teacher/attendance/<int:class_subject_id>/<str:date>/', views.TeacherAttendanceDetailView.as_view(), name='teacher_attendance_detail'),
    path('teacher/grades/', views.TeacherGradesView.as_view(), name='teacher_grades'),
    
    # API Endpoints
    path('api/attendance/<int:class_subject_id>/<str:date>/', views.AttendanceAPIView.as_view(), name='attendance_api'),
    path('api/grades/<int:class_id>/<str:assessment_type>/', views.GradesAPIView.as_view(), name='grades_api'),
    
    # Student Views
    path('student/classes/', views.StudentClassListView.as_view(), name='student_classes'),
    path('student/attendance/', views.StudentAttendanceView.as_view(), name='student_attendance'),
    path('student/grades/', views.StudentGradesView.as_view(), name='student_grades'),
    
    # Parent Views
    path('parent/children/', views.ChildrenListView.as_view(), name='children_list'),
    path('parent/children/attendance/', views.ChildrenAttendanceView.as_view(), name='children_attendance'),
    path('parent/children/grades/', views.ChildrenGradesView.as_view(), name='children_grades'),
    
    # Class Subject Management
    path('class-subject/<int:pk>/edit/', views.ClassSubjectUpdateView.as_view(), name='class_subject_update'),
]
