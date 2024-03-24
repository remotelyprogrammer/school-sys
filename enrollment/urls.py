from django.urls import path
from . import views
from .views import EnrollmentHomeView

app_name = 'enrollment'

urlpatterns = [
    path('', EnrollmentHomeView.as_view(), name='enrollment-home'),
    path('create/', views.CreateEnrollmentView.as_view(), name='enrollment-create'),
    path('student-autocomplete/', views.EnrollmentAutoComplete.as_view(), name='student-autocomplete'),
    path("<int:pk>/", views.EnrollmentDetailView.as_view(), name="enrollee-detail"),
    path("list/", views.EnrollmentListView.as_view(), name="enrollment-list"),

    path('create-school-year/', views.CreateSchoolYearView.as_view(), name='school-year-create'),
    path('school-year/<int:pk>/', views.SchoolYearDetailView.as_view(), name='school-year-detail'),
    path("school-year-list/", views.SchoolYearListView.as_view(), name="school-year-list"),

    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject-create'),


    path('curriculum/', views.CurriculumListView.as_view(), name='curriculum-list'),
    path('curriculum/new/', views.curriculum_create_or_update, name='curriculum-create'),
    path('curriculum/<int:curriculum_id>/edit/', views.curriculum_create_or_update, name='curriculum_edit'),

]



    
