from django.urls import path

from courses.views import (experiments_view, ManageCourseListView,
                           CourseCreateView, CourseUpdateView,
                           CourseDeleteView, CourseModuleUpdateView,
                           ContentCreateUpdateView, ContentDeleteView,
                           ModuleContentListView, ModuleOrderView,
                           ContentOrderView, CourseListView,
                           CourseDetailView, )

app_name = 'courses'

urlpatterns = [
    # -------------------CMS:
    # course read/create/update/delete views:
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/module/', CourseModuleUpdateView.as_view(), name='course_module_update'),

    # content create/update/delete/read/ views:
    path('module/<int:module_id>/content/<str:model_name>/create/',  # - create
         ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<str:model_name>/<int:pk>/',  # - update
         ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('module/<int:pk>/delete/', ContentDeleteView.as_view(), name='module_content_delete'),  # - delete
    path('module/<int:module_id>/', ModuleContentListView.as_view(), name='module_content_list'),  # - read (list)

    # order views:
    path('module/order/', ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', ContentOrderView.as_view(), name='content_order'),

    # -------------------FOR STUDENTS (NOT CMS):
    # course read - list, list with subject, detail
    path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),

    # experiments:
    path('experiments/', experiments_view, name='experiments'),
]
