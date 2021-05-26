from django.urls import path

from courses.views import experiments_view

app_name = 'courses'

urlpatterns = [
    path('experiments/', experiments_view, name='experiments'),
]
