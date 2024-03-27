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
    path('curriculum/create', views.CurriculumCreateView.as_view(), name='curriculum-create'),

    path('curriculumset/new/', views.curriculumset_create_or_update, name='curriculumset-create'),
    path('curriculumset/<int:curriculum_id>/edit/', views.curriculumset_create_or_update, name='curriculumset_edit'),

    path('grade-level/create/', views.GradeLevelCreateView.as_view(), name='grade-level-create'),
    path('grade-level/list/', views.GradeLevelListView.as_view(), name='grade-level-list'),

]



    
