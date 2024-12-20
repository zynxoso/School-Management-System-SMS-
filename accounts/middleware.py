from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_type = request.user.user_type
            current_path = request.path_info

            # Define restricted paths for each user type
            admin_only_paths = [
                '/admin/',
                '/settings/',
                '/users/manage/',
            ]

            teacher_paths = [
                '/classes/',
                '/grades/',
                '/attendance/',
            ]

            student_paths = [
                '/courses/',
                '/assignments/',
                '/grades/view/',
            ]

            parent_paths = [
                '/children/',
                '/progress/',
                '/meetings/',
            ]

            # Check permissions based on user type
            if user_type != 'admin' and any(current_path.startswith(path) for path in admin_only_paths):
                messages.error(request, 'You do not have permission to access this area.')
                return redirect('dashboard')

            if user_type == 'student' and any(current_path.startswith(path) for path in teacher_paths):
                messages.error(request, 'Only teachers can access this area.')
                return redirect('dashboard')

            if user_type == 'parent' and any(current_path.startswith(path) for path in teacher_paths + student_paths):
                messages.error(request, 'Parents cannot access this area.')
                return redirect('dashboard')

        response = self.get_response(request)
        return response
