from django.forms import Form, ModelChoiceField, HiddenInput

from courses.models import Course


class CourseEnrollForm(Form):
    course = ModelChoiceField(queryset=Course.objects.all(), widget=HiddenInput)
