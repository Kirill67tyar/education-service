from rest_framework import routers

from django.urls import path, include

from courses.api.views import (SubjectDetailAPIView,
                               SubjectListAPIView,
                               CourseDetailAPIView,
                               CourseListAPIView,
                               CourseEnrollAPIView,
                               CourseViewSet, )

app_name = 'api'

router = routers.DefaultRouter()

router.register(prefix='courses', viewset=CourseViewSet, basename='courses')

urlpatterns = [
    # subjects API
    path('subjects/<int:pk>/', SubjectDetailAPIView.as_view(), name='subject_detail_api'),
    path('subjects/', SubjectListAPIView.as_view(), name='subject_list_api'),

    # courses API
    # path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail_api'),
    # path('courses/', CourseListAPIView.as_view(), name='course_list_api'),
    path('courses/<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='course_enroll_api'),

    # для router от DRF
    path('', include(router.urls)),

]
"""
routers

https://www.django-rest-framework.org/api-guide/routers/
https://www.django-rest-framework.org/api-guide/viewsets/

Стоит заметить, то этот роутер работает скорее всего только с ViewSet
Непонятно то там с именами шаблонов (path_name).

А так алгоритм простой:
1) импортирум DefaultRouter
2) создаем экземпляр этого класса (router = DefaultRouter())
3) используем метод register(prefix='', viewset=...ViewSet, basename=None)
4) можно установить basename и будет какое-то базовое namespace для этих обработчиков 
5) делаем или так: 
    urlpatterns = router.urls
    или так: 
    urlpatterns.append(path('', include(router.urls)))
    
Не люблю совсем уж такие автоматизированные штуки.

Маршрутизатор автоматически сформирует необходимые URL'ы
И будет передавать запрос в подходящий обработик
"""
