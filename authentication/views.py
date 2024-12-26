from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTTokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter
from utils.util_functions import generate_passwords

# , , InstructorSerializer
from .serializers import UserSerializer, TokenObtainSerializer, ProgramSerializer, StudentSerializer, InstructorSerializer

from course.models import Course, StudentCourse
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
        generated_password = generate_passwords()

        serializer = UserSerializer.UserCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        message = f"""
            Your account details are
            password: {generated_password}
            """
        user.email_user("Roothub Account Login Credentials",
                            message, "admin@developer.com")
        
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
        generated_password = generate_passwords()

        # a signal is been triggered to add user to a course session
        serializer = StudentSerializer.StudentCreateSerializer(
            data=copy_data, 
            context={"generated_password": generated_password}
        )
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        # add student to course
        prog = student.program
        course = prog.courses.all().order_by('level').first()

        if(course):
            StudentCourse.objects.create(
                student=student,
                course=course
            )

        message = f"""
        Your account details are
        password: {generated_password}
        """
        student.user.email_user("Roothub Account Login Credentials",
                        message, "admin@developer.com")
        
        #TODO: send notification to instructor of the course

        message = f"Student registration is successful, user credentials has been sent to {copy_data['user']['email']}"
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
        generated_password = generate_passwords()

        serializer = InstructorSerializer.InstructorCreateSerializer(
            data=copy_data)
        serializer.is_valid(raise_exception=True)
        instructor = serializer.save()

        message = f"""
            Your account details are
            password: {generated_password}
        """

        instructor.user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
                    
        message = f"Instructor registration is successful, user credentials has been sent to {
            copy_data['user']['email']}"
        return Response({"detail": message}, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def reset_password(self, request, *args, **kwargs):
        serializer = UserSerializer.ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            reset_url = f"{settings.PASSWORD_RESET_BASE_URL}/{token}"
            subject = "Password Reset Request"
            message = f"Hi {user.first_name},\n\nPlease click the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."
            email_from = settings.DEFAULT_FROM_EMAIL

            user.email_user(subject, message, email_from)

            return Response({'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


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
