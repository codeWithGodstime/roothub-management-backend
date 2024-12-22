from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTTokenObtainPairView

from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter

# , , InstructorSerializer
from .serializers import UserSerializer, TokenObtainSerializer, ProgramSerializer, StudentSerializer, InstructorSerializer

from course.models import Course
from .models import Program, Student, Instructor


User = get_user_model()


class CustomUserAccountCreatePermission(permissions.BasePermission):
    """
    Custom permission to allow only superusers to create staff accounts
    and staff to create student accounts.
    """

    def has_permission(self, request, view):
        """
        Custom permission logic for role-based user creation.
        Assumes separate endpoints for staff and student creation.
        """

        # Allow only authenticated users to proceed
        if not request.user.is_staff or not request.user.is_authenticated:
            return False

        if view.action == "create":
            if request.user.is_superuser:
                # Superusers can create all accounts
                return True

            if view.action == "students" and request.user.is_staff:
                # Staff can create student accounts
                return True

            # Deny if the action does not match permissions
            return False

        # Return True for other actions like get
        return True


class CustomAdminOnlyPermission(permissions.BasePermission):
    """
    Custom permission to allow only superusers to create staff accounts
    and staff to create student accounts.
    """

    def has_permission(self, request, view):
        """
        Permission for only superadmin users
        """
        # Allow only authenticated users to proceed
        if request.user.is_superuser:
            return True
        return False


@extend_schema(tags=['Users'])
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer.UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated,
                          CustomUserAccountCreatePermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset  # Admin users can see all users
        return self.queryset.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        copy_data = request.data.copy()

        serializer = UserSerializer.UserCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = f"User registration is successful, user credentials has been sent to {
            copy_data['email']}"

        return Response({"detail": message}, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="create students",
        request=StudentSerializer.StudentCreateSerializer,
        summary="Create a student account endpoint"
    )
    @action(methods=["post"], detail=False)
    @transaction.atomic()
    def students(self, request, *args, **kwargs):
        copy_data = request.data.copy()

        # a signal is been triggered to add user to a course session
        serializer = StudentSerializer.StudentCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        # add student to course

        prog = student.program
        course = prog.courses.all().order_by('level').first()

        if(course):
            student.courses.add(course)

        # TODO: move sending of email from serializer to view
        
        #TODO: send notification to instructor of the course


        message = f"Student registration is successful, user credentials has been sent to {
            copy_data['user']['email']}"
        return Response({"detail": message}, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="create instructors",
        request=InstructorSerializer.InstructorCreateSerializer,
        summary="Create a instructor account endpoint"
    )
    @action(methods=['post'], detail=False)
    @transaction.atomic()
    def instructors(self, request, *args, **kwargs):
        copy_data = request.data.copy()

        serializer = InstructorSerializer.InstructorCreateSerializer(
            data=copy_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = f"Instructor registration is successful, user credentials has been sent to {
            copy_data['user']['email']}"
        return Response({"detail": message}, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Program'])
class ProgramViewset(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer.ProgramRetrieveSerializer
    permission_classes = [
        permissions.IsAuthenticated, CustomAdminOnlyPermission]

    @extend_schema(
        operation_id="Create program",
        request=ProgramSerializer.ProgramCreateSerializer,
        summary="Create a program account endpoint"
    )
    @transaction.atomic()
    def create(self, request, *args, **kwargs):

        # program = super().create(request, *args, **kwargs)
        serializer = ProgramSerializer.ProgramRetrieveSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        program = serializer.save()

        levels = ["basic", "intermediate", "advanced"]
        if program.duration == 4:
            levels = ["beginner", "basic", "intermediate", "advanced"]

        # create course
        for t in range(program.duration):
            Course.objects.create(
                name=f"{program.name}-{levels[t]}",
                program=program,
                duration=str(1),  # every course last for atleast a month
                level=t
            )

        response_data = ProgramSerializer.ProgramRetrieveSerializer(
            program).data

        return Response(response_data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="Update Program",
        request=ProgramSerializer.ProgramUpdateSerializer,
        summary="Update program information by the admin"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


@extend_schema(tags=['Students'])
class StudentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer.StudentRetrieveSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


@extend_schema(tags=['Instructors'])
class InstructorViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer.InstructorRetrieveSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
