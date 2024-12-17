DJANGO PROJECT:

JAN HARRY I MADRONA
RAYSON JAMES IMBAG
ZAEREL ALFRED CASTILLO

# School Management System (SMS)

A comprehensive web-based school management system built with Django, designed to streamline educational institution management.

## 🎯 Features

### User Management
- **Multi-role Authentication**
  - Admin
  - Teachers
  - Students
- **Secure Login System**
  - Password reset functionality
  - Remember me option
  - Session management

### Academic Management
- **Class Management**
  - Create and manage classes
  - Assign class teachers
  - Set class capacity
  - Track academic years
- **Subject Management**
  - Add/Edit subjects
  - Assign teachers to subjects
  - Track subject progress

### Student Management
- **Student Profiles**
  - Personal information
  - Academic records
  - Grade management
- **Enrollment Management**
  - Class assignments
  - Subject registration
  - Transfer management

### Teacher Management
- **Teacher Profiles**
  - Professional information
  - Subject expertise
  - Class assignments
- **Teaching Load**
  - Schedule management
  - Subject assignments
  - Class responsibilities

### Grading System
- **Grade Management**
  - Record and manage grades
  - Calculate GPA/percentages
  - Generate report cards
- **Assessment Tools**
  - Create assessments
  - Track student progress
  - Performance analytics

### Administrative Features
- **Dashboard**
  - Overview statistics
  - Quick actions
  - Recent activities
- **Reports Generation**
  - Academic reports
  - Performance analytics

## 🚀 Technology Stack

- **Backend**
  - Django 4.x
  - Python 3.x
  - SQLite/PostgreSQL

- **Frontend**
  - HTML5
  - CSS3 (Bootstrap 5.3)
  - JavaScript
  - Material Icons
  - Google Fonts (Poppins)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SMS.git
cd SMS
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## 📁 Project Structure

```
SMS/
├── accounts/          # User authentication and management
├── academic/          # Academic-related functionality
├── student/           # Student management
├── teacher/           # Teacher management
├── attendance/        # Attendance tracking
├── grading/          # Grade management
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
└── sms/              # Project configuration
```

## 🔐 Security Features

- CSRF protection
- Password hashing
- Session security
- Form validation
- XSS prevention
- SQL injection protection

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- JAN HARRY MADRONA - https://github.com/zynxoso

## 🙏 Acknowledgments

- Bootstrap team for the amazing UI framework
- Django community for the robust backend framework
- All contributors who have helped shape this project

## 📞 Support

For support, email janharrymadrona@gmail.com or create an issue in the repository.
