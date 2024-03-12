from django.urls import path
from . import views
from .views import EnrollmentHomeView

app_name = 'enrollment'

urlpatterns = [
    path('', EnrollmentHomeView.as_view(), name='enrollment-home'),
    path('create/', views.CreateEnrollmentView.as_view(), name='enrollment-create'),
    path('student-autocomplete/', views.EnrollmentAutoComplete.as_view(), name='student-autocomplete'),
    path("<int:pk>/", views.EnrollmentDetailView.as_view(), name="enrollee-detail"),
    path("list/", views.EnrollmentListView.as_view(), name="enrollment-list")


]