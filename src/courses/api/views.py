from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     get_object_or_404, )

from courses.models import Subject, Course
from courses.api.serializers import (SubjectModelSerializer,
                                     CourseModelSerializer, )


class SubjectDetailAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer


class SubjectListAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer

# --------------------------------------------
# --- такой способ показать курсы (list и retrieve)
class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer

#           ^--^--^ OR v--v--v

# --- или такой, с помощью ViewSet
class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer

# ---------------------------------------------

class CourseEnrollAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        user = request.user
        if user not in course.students.all():
            course.students.add(user)
            return Response({'Enrolled': True, })
        return Response({'Enrolled': True, 'Already recorded': True, })
