from django.db import models
from student.models import Student
from django.utils import timezone


class GradeLevel(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of the grade level")
    order = models.PositiveIntegerField(help_text="The order in which the grade level appears")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class SchoolYear(models.Model):
    start_year = models.PositiveSmallIntegerField(help_text="The start year of the school year, e.g., 2024")
    end_year = models.PositiveSmallIntegerField(help_text="The end year of the school year, e.g., 2025")
    is_current = models.BooleanField(default=False, help_text="Indicates if this is the current school year")

    class Meta:
        ordering = ['-start_year']  # Orders the school years in descending order by start year
        unique_together = (('start_year', 'end_year'),)  # Ensures the combination of start and end year is unique

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure no other SchoolYear is marked as current
            SchoolYear.objects.filter(is_current=True).update(is_current=False)
        super(SchoolYear, self).save(*args, **kwargs)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name='enrollments')
    enrollment_number = models.AutoField(primary_key=True)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('school_year', 'enrollment_number'),)

    @property
    def school_year_id(self):
        # Extract the last two digits of the start and end years
        year_prefix = f"{str(self.school_year.start_year)[-2:]}{str(self.school_year.end_year)[-2:]}"
        return f"{year_prefix}-{self.enrollment_number:07d}"

    def __str__(self):
        # Same logic in the __str__ method
        year_prefix = f"{str(self.school_year.start_year)[-2:]}{str(self.school_year.end_year)[-2:]}"
        return f"{year_prefix}-{self.enrollment_number:07d}"

