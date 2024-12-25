from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter

from .serializers import CourseSerializer, CourseSessionSerializer
from .permissions import IsAdminOrInstructorForSession
from .models import Course, CourseSession, StudentCourseSession, StudentCourse



# @extend_schema(tags=['CourseSession'])
# class CourseSessionViewset(viewsets.ModelViewSet):
#     queryset = CourseSession.objects.all()
#     serializer_class = CourseSessionSerializer.CourseSessionRetrieveSerializer
#     permission_classes = [IsAdminOrInstructorForSession, permissions.IsAuthenticated]

#     @extend_schema(
#             request=StudentCourseSessionSerializer.StudentCourseSessionCreateSerializer, 
#             responses=CourseSessionSerializer.CourseSessionRetrieveSerializer
#     )
#     @action(methods=['post'], detail=True)
#     def add(self, request, *args, **kwargs):
#         session = self.get_object()
#         serializer = StudentCourseSessionSerializer.StudentCourseSessionCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         session = serializer.save()
#         serialized_session = CourseSessionSerializer.CourseSessionRetrieveSerializer(data=session).data
#         return Response(serialized_session, status=status.HTTP_200_OK)


@extend_schema(tags=['Course'])
class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer.CourseRetrieveSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    @extend_schema(
        request=CourseSerializer.CourseCreateSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="assign instructor to course",
        request=CourseSerializer.AssignInstructorToCourse,
        summary="Admin can assign instructor to a course"
    )
    @action(methods=['post'], detail=True)
    def assign(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseSerializer.AssignInstructorToCourse(
            data=request.data,
            context={'course': course}
        )
        serializer.is_valid(raise_exception=True)
        course = serializer.save()

        serialized_response = CourseSerializer.CourseRetrieveSerializer(
            course).data
        return Response(serialized_response, status=status.HTTP_200_OK)


# class StudentCourseSessionViewset(viewsets.ModelViewSet):
#     queryset = StudentCourseSession.objects.all()
#     permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
#     serializer_class = StudentCourseSessionSerializer.StudentCourseSessionRetrieveSerializer

