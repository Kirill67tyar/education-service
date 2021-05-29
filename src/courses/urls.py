from django.urls import path

from courses.views import (experiments_view,
                           ManageCourseListView,
                           CourseCreateView,
                           CourseUpdateView,
                           CourseDeleteView,
                           CourseModuleUpdateView,
                           ContentCreateUpdateView, )

app_name = 'courses'

urlpatterns = [
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/module/', CourseModuleUpdateView.as_view(), name='course_module_update'),

    # content create/update
    path('module/<int:module_id>/content/<str:model_name>/create/',
         ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<str:model_name>/<int:pk>/',
         ContentCreateUpdateView.as_view(), name='module_content_update'),

    # experiments
    path('experiments/', experiments_view, name='experiments'),
]
