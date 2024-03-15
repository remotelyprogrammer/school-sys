# Generated by Django 4.2.1 on 2024-03-15 14:51

from django.db import migrations


def set_grade_level_to_grade_2(apps, schema_editor):
    GradeLevel = apps.get_model('enrollment', 'GradeLevel')
    Enrollment = apps.get_model('enrollment', 'Enrollment')

    # First, get the GradeLevel instance for 'Grade 2'.
    # If it does not exist, create it.
    grade_2, created = GradeLevel.objects.get_or_create(name='Grade 2')

    # Now update the enrollments to have 'Grade 2' as their grade level.
    Enrollment.objects.all().update(grade_level=grade_2)


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0004_gradelevel_alter_enrollment_grade_level'),
    ]

    operations = [
        migrations.RunPython(set_grade_level_to_grade_2),
    ]
