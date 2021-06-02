from django.urls import path

from students.views import (StudentRegistrationView,
                            SrudentEnrollCourseView,
                            StudentCourseListView,
                            StudentCourseDetailView, )

app_name = 'students'

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', SrudentEnrollCourseView.as_view(), name='student_enroll_course'),

    # student course list/detail
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<int:pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>/', StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
]
