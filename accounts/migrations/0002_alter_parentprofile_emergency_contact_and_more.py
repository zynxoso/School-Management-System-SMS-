# Generated by Django 4.2.16 on 2024-12-14 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parentprofile",
            name="emergency_contact",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name="parentprofile",
            name="occupation",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="parentprofile",
            name="relationship",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="teacherprofile",
            name="department",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="teacherprofile",
            name="employee_id",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="teacherprofile",
            name="joining_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="teacherprofile",
            name="qualification",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "student_id",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("admission_date", models.DateField(blank=True, null=True)),
                ("current_class", models.CharField(blank=True, max_length=50)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"user_type": "parent"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
