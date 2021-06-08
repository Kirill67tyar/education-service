from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     get_object_or_404, )

from courses.models import Subject, Course
from courses.api.permissions import IsEnrolled
from courses.api.serializers import (SubjectModelSerializer,
                                     CourseModelSerializer,
                                     ThinCourseSerializer,
                                     CourseWithContentsSerializer, )


class SubjectDetailAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer


class SubjectListAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer


# ---------------------------------------------------------------------------
# --- такой способ показать курсы (list и retrieve)
class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer


class CourseEnrollAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        user = request.user
        if user not in course.students.all():
            course.students.add(user)
            return Response({'Enrolled': True, })
        return Response({'Already enrolled': True, })


#                                     ^--^--^ OR v--v--v

# --- или такой, с помощью ViewSet (кстати ViewSet - тоже через list и retrieve)
class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ThinCourseSerializer

    @action(detail=True,
            methods=['post', ],
            authentication_classes=[BasicAuthentication, ],
            permission_classes=[IsAuthenticated, ])
    def enroll(self, request, *args, **kwargs):
        user = request.user
        course = self.get_object()
        if user not in course.students.all():
            course.students.add(user)
            return Response({'Enrolled': True, })
        return Response({'Already enrolled': True, })

    @action(detail=True,
            methods=['get', ],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication, ],
            permission_classes=[IsAuthenticated, IsEnrolled, ])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return ThinCourseSerializer
    #     return CourseWithContentsSerializer

# благодаря декоратору @action мы смогли реализовать адрес url через роутер
# как django поймет, какой имя (path_name) у этого обработчика?
# благодаря названию функции, над которой стоит декоратор.
# url будет выгляить так для этого обработчика - reverse(api:courses-enroll)
# ---------------------------------------------------------------------------
