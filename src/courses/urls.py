from django.urls import path

from courses.views import (experiments_view,
                           ManageCourseListView,
                           CourseCreateView,
                           CourseUpdateView,
                           CourseDeleteView, )

app_name = 'courses'

urlpatterns = [
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # experiments
    path('experiments/', experiments_view, name='experiments'),
]
