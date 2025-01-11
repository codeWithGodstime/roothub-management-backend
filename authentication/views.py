import logging
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTTokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter
from utils.util_functions import generate_passwords
from utils.permissions import IsAdminOrInstructorForSession

from .serializers import UserSerializer, TokenObtainSerializer, ProgramSerializer, StudentSerializer, InstructorSerializer
from .filters import StudentFilter

from course.models import Course, StudentCourse, CourseSession
from course.serializers import CourseSessionSerializer

from .models import Program, Student, Instructor


logger = logging.getLogger(__name__)

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
        logger.info(f"User registration attempt with data: {request.data}")

        copy_data = request.data.copy()
        generated_password = generate_passwords()
        logger.debug(f"Generated password for new user: {generated_password}")

        serializer = UserSerializer.UserCreateSerializer(data=copy_data)
        if serializer.is_valid(raise_exception=True):
            logger.info(f"User data validated successfully.")
            user = serializer.save()
            logger.info(f"User created successfully with ID: {user.id}")

            message = f"""
                Your account details are
                password: {generated_password}
            """
            logger.info(f"Sending email to user: {user.email}")
            user.email_user("Roothub Account Login Credentials",
                            message, "admin@developer.com")
            logger.info(f"Email sent successfully to: {user.email}")

            message = f"User registration is successful, user credentials have been sent to {copy_data['email']}"
            logger.info(message)
            return Response({"detail": message}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"User registration failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        operation_id="create students",
        request=StudentSerializer.StudentCreateSerializer,
        summary="Create a student account endpoint"
    )
    @action(methods=["post"], detail=False)
    @transaction.atomic()
    def students(self, request, *args, **kwargs):
        logger.info(f"Student registration attempt with data: {request.data}")

        copy_data = request.data.copy()
        generated_password = generate_passwords()
        logger.debug(f"Generated password for new student: {generated_password}")

        serializer = StudentSerializer.StudentCreateSerializer(
            data=copy_data,
            context={"generated_password": generated_password}
        )
        if serializer.is_valid(raise_exception=True):
            logger.info(f"Student data validated successfully.")
            student = serializer.save()
            logger.info(f"Student created successfully with ID: {student.id}")

            prog = student.program
            course = prog.courses.all().order_by('level').first()
            if course:
                logger.info(f"Assigning student {student.id} to course {course.id}")
                # m2m relationship
                StudentCourse.objects.create(
                    student=student,
                    course=course
                )
                logger.info(
                    f"Student {student.id} added to course {course.id}")

            message = f"""
                Your account details are
                password: {generated_password}
            """
            logger.info(f"Sending email to student: {student.user.email}")
            student.user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
            logger.info(f"Email sent successfully to: {student.user.email}")

            # TODO: Send notification to instructor of the course
            logger.info(f"Notification to instructor about student {student.id} needs to be sent.")

            message = f"Student registration is successful, user credentials have been sent to {copy_data['user']['email']}"
            logger.info(message)
            return Response({"detail": message}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Student registration failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        operation_id="create instructors",
        request=InstructorSerializer.InstructorCreateSerializer,
        summary="Create a instructor account endpoint"
    )
    @action(methods=['post'], detail=False)
    @transaction.atomic()
    def instructors(self, request, *args, **kwargs):
        logger.info(f"Instructor registration attempt with data: {request.data}")

        copy_data = request.data.copy()
        generated_password = generate_passwords()
        logger.debug(f"Generated password for new instructor: {generated_password}")

        serializer = InstructorSerializer.InstructorCreateSerializer(
            data=copy_data, context={"generated_password": generated_password})
        if serializer.is_valid(raise_exception=True):
            logger.info(f"Instructor data validated successfully.")
            instructor = serializer.save()
            logger.info(f"Instructor created successfully with ID: {instructor.id}")

            message = f"""
                Your account details are
                password: {generated_password}
            """
            logger.info(f"Sending email to instructor: {instructor.user.email}")
            instructor.user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
            logger.info(f"Email sent successfully to: {instructor.user.email}")

            message = f"Instructor registration is successful, user credentials have been sent to {copy_data['user']['email']}"
            logger.info(message)
            return Response({"detail": message}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Instructor registration failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def reset_password(self, request, *args, **kwargs):
        logger.info(f"Password reset request with data: {request.data}")

        serializer = UserSerializer.ResetPasswordRequestSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data["email"]
            user = User.objects.filter(email__iexact=email).first()

            if user:
                logger.info(f"User found for email: {email}, initiating password reset.")
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                logger.debug(f"Generated token: {token}")

                reset_url = f"{
                    settings.PASSWORD_RESET_BASE_URL}/{user.id}:{token}"
                logger.info(f"Password reset URL: {reset_url}")

                subject = "Password Reset Request"
                message = f"Hi {user.first_name},\n\nPlease click the link below to reset your \npassword:{reset_url}\n\nIf you did not request this, please ignore this email."
                email_from = settings.DEFAULT_FROM_EMAIL

                logger.info(f"Sending password reset email to: {email}")
                user.email_user(subject, message, email_from)
                logger.info(f"Password reset email sent successfully to: {email}")

                return Response({'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"User with email {email} not found.")
                return Response({"error": "User with email not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f"Password reset request failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def change_password(self, request, *args, **kwargs):
        logger.info(f"Password change request with data: {request.data}")

        serializer = UserSerializer.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Password change request validated successfully.")
            serializer.save()
            logger.info(f"Password changed successfully for user: {self.request.user.id}")
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Password change request failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        logger.info(f"Program creation request with data: {request.data}")

        serializer = ProgramSerializer.ProgramRetrieveSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        program = serializer.save()

        logger.info(f"Program '{program.name}' created successfully with ID {program.id}.")

        levels = ["beginner", "basic", "intermediate", "advanced"]
        logger.info(f"Creating courses for program '{program.name}' with levels: {levels}")

        # Create courses
        if program.duration == 3:
        
            for i in range(1, program.duration + 1):
                course_name = f"{program.name}-{levels[i]}"
                Course.objects.create(
                    name=course_name,
                    program=program,
                    duration=str(1),  # every course lasts for at least a month
                    level=i
                )
                logger.info(f"Course '{course_name}' created successfully.")
        else:
            for i in range(program.duration):
                course_name = f"{program.name}-{levels[i]}"
                Course.objects.create(
                    name=course_name,
                    program=program,
                    duration=str(1),  # every course lasts for at least a month
                    level=i
                )
                logger.info(f"Course '{course_name}' created successfully.")

        response_data = ProgramSerializer.ProgramRetrieveSerializer(
            program).data
        logger.info(f"Program creation response: {response_data}")

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

@extend_schema(tags=['Instructors'])
class InstructorViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer.InstructorRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        responses=CourseSessionSerializer.CourseSessionRetrieveSerializer(
            many=True)
    )
    @action(methods=["GET"], detail=True)
    def active_sessions(self, request, *args, **kwargs):
        instructor = self.get_object()

        # Check if the logged-in user is the instructor
        if instructor.user != request.user:
            raise PermissionDenied(
                "You do not have permission to view these sessions.")

        sessions = CourseSession.objects.filter(course__instructor=instructor)
        serializer = CourseSessionSerializer.CourseSessionRetrieveSerializer(
            sessions, many=True)

        page = self.paginate_queryset(sessions)
        if page is not None:
            serializer = CourseSessionSerializer.CourseSessionRetrieveSerializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback if pagination is not enabled
        serializer = CourseSessionSerializer.CourseSessionRetrieveSerializer(
            sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@extend_schema_view(tags=["Analytics"])
class AdminAnalyticsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    @extend_schema(
        responses={
            "student_count": 0,
            "instructor_count": 0,
            "courseCount": 0
        }
    )
    @action(methods=['GET'], detail=False)
    def dashboard_summary(self, request, *args, **kwargs):
        studentCount = Student.objects.all().count()
        instructorCount = Instructor.objects.all().count()
        programCount = Program.objects.all().count()

        return Response(
            [
                {
                    "count": studentCount,
                    "text": "Total Students"
                },
                {
                    "count": instructorCount,
                    "text": "Total Instructors"
                },
                {
                    "count": programCount,
                    "text": "Total Programs"
                },
            ],
            status=status.HTTP_200_OK
        )
