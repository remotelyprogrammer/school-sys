from django.urls import path
from . import views
from .views import home, add_student_contacts

app_name = 'student'

urlpatterns = [
    path('create/', views.CreateStudentView.as_view(), name='create-student'),
    path('', home, name='student-home'),
    path('<int:pk>/add-contacts/', add_student_contacts, name='add-contacts'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),

]