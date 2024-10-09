from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTTokenObtainPairView

from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiParameter

from .serializers import UserSerializer, TokenObtainSerializer

User = get_user_model()

@extend_schema(tags=['Users'])
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer.UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        copy_data = request.data.copy()

        serializer = UserSerializer.UserCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = f"User registration is successful, user credentials has been sent to {copy_data['email']}"

        return Response({"detail": message}, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id="create students",
            request=UserSerializer.StudentUserCreateSerializer,
            summary="Create a student account endpoint"
    )
    @action(methods=["post"], detail=False)
    def students(self, request, *args, **kwargs):
        copy_data = request.data.copy()
        
        serializer = UserSerializer.StudentUserCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message =  f"Student registration is successful, user credentials has been sent to {copy_data['email']}"
        return Response({"detail": message}, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id="create instructors",
            request=UserSerializer.InstructorUserCreateSerializer,
            summary="Create a instructor account endpoint"
    )
    @action(methods=['post'], detail=False)
    def instructors(self, request, *args, **kwargs):
        copy_data = request.data.copy()
        
        serializer = UserSerializer.InstructorUserCreateSerializer(data=copy_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = f"Instructor registration is successful, user credentials has been sent to {copy_data['email']}"
        return Response({"detail": message}, status=status.HTTP_201_CREATED)
    

class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:

        return super().post(request, *args, **kwargs)