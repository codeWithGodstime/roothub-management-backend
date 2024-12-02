# from rest_framework import viewsets, permissions
# from rest_framework.decorators import action
# from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter

# from .serializers import CourseSerializer, CourseSessionSerializer
# from .models import Course, CourseSession

# @extend_schema(tags=['Course session'])
# class CourseSessionViewset(viewsets.ModelViewSet):
#     queryset = CourseSession.objects.all()
#     serializer_class = CourseSessionSerializer.CourseSessionRetreiveSerializer
#     permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


# @extend_schema(tags=['Course'])
# class CourseViewset(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer.CourseRetrieveSerializer
#     permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

#     @extend_schema(
#             request=CourseSerializer.CourseCreateSerializer
#     )
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

#     @extend_schema(
#             responses=CourseSessionSerializer.CourseSessionUnassignedSerializer(many=True)
#     )
#     @action(methods=['get'], detail=True)
#     def unassigned_course_session(self, request, pk=None, *args, **kwargs):
#         """get all unasigned session for a course"""
#         course = self.get_object()
#         unassigned_sessions = course.sessions.filter(instructor=None)
#         serializer = CourseSessionSerializer.CourseSessionUnassignedSerializer(unassigned_sessions).data

#         return serializer



    