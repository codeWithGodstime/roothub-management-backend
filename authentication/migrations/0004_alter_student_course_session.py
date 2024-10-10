# Generated by Django 5.1.2 on 2024-10-10 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_student_course_session'),
        ('course', '0003_remove_coursesession_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='course.coursesession', verbose_name='students'),
        ),
    ]
