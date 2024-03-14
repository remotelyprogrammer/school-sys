from django.db import models
from student.models import Student
from django.utils import timezone

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
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    enrollment_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('school_year', 'enrollment_number'),)

    def __str__(self):
        year_prefix = f"{self.school_year.start_year}{self.school_year.end_year}"[:4]  # Example format: 2425
        return f"{year_prefix}-{self.enrollment_number:07d}"

    @property
    def school_year_id(self):
        year_prefix = f"{self.school_year.start_year}{self.school_year.end_year}"[:4]  # Example format: 2425
        return f"{year_prefix}-{self.enrollment_number:07d}"