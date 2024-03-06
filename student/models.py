from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max, Q


class Student(models.Model):
    std_sch_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField()
    country_of_birth = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    CIVIL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
    ]
    civil_status = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES, blank=True)

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)
    religion = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=20, blank=True)
    personal_email = models.EmailField()

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', help_text="Student's account status")

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"


class Address(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    barangay = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.house_number} {self.barangay}, {self.city}, {self.province}"


class Contact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='contacts')
    full_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.relationship} to {self.student.first_name}"
