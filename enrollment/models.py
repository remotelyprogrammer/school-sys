from django.db import models
from student.models import Student
from django.utils import timezone
from django.db.models import Max


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


class Curriculum(models.Model):
    curriculum_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.curriculum_name}"


class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Unique code for the subject, e.g., MATH101")
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, help_text="Name of the subject, e.g., Mathematics")
    description = models.TextField(blank=True, help_text="A brief description of the subject")

    def __str__(self):
        return f"{self.code} - {self.name}"


class GradeLevel(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="The name of the grade level, e.g., Grade 1")
    order = models.PositiveIntegerField(help_text="The order in which the grade level appears")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name='enrollments')
    enrollment_number = models.IntegerField()
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('school_year', 'enrollment_number'),)

    @property
    def school_year_reg(self):
        # Extract the last two digits of the start and end years
        year_prefix = f"{str(self.school_year.start_year)[-2:]}{str(self.school_year.end_year)[-2:]}"
        return f"{year_prefix}-{self.enrollment_number:07d}"

    def __str__(self):
        # Same logic in the __str__ method
        year_prefix = f"{str(self.school_year.start_year)[-2:]}{str(self.school_year.end_year)[-2:]}"
        return f"{year_prefix}-{self.enrollment_number:07d}"

    def save(self, *args, **kwargs):
        # If this is a new enrollment (i.e., it doesn't have an ID yet)
        if not self.id:
            # Get the current maximum enrollment number for the school year
            current_max = Enrollment.objects.filter(school_year=self.school_year).aggregate(Max('enrollment_number'))['enrollment_number__max']
            
            # If there are no enrollments yet for the school year, start at 1. Otherwise, increment by 1.
            self.enrollment_number = 1 if current_max is None else current_max + 1
        
        super(Enrollment, self).save(*args, **kwargs)
