from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer
from faker import Faker

from .models import User, Student, Instructor
from utils.util_functions import generate_passwords

User = get_user_model()
faker = Faker()


class UserSerializer:
    class UserCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("email", "first_name", "last_name")

        def create(self, validated_data):
            generated_password = generate_passwords()
            user = User.objects.create_user(password=generated_password, **validated_data)

            message = f"""
            Your account details are
            password: {generated_password}
            """
            user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
            user.save()
            return user

    class InstructorUserCreateSerializer(UserCreateSerializer):
        
        def create(self, validated_data):
            generated_password = generate_passwords()
            user = User.objects.create_instructor(password=generated_password, **validated_data)

            message = f"""
            Your account details are
            password: {generated_password}
            """
            user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
            user.save()
            return user
    
    class StudentUserCreateSerializer(UserCreateSerializer):

        def create(self, validated_data):
            generated_password = generate_passwords()
            user = User.objects.create_student(password=generated_password, **validated_data)
            user.save()
            return user

    
    class UserRetrieveSerializer(serializers.ModelSerializer):

        user_type_info = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = (
                "email", 
                "first_name", 
                "last_name", 
                "user_type_info"
            )
        
        def get_user_type_info(self, obj):
            if obj.is_student:
                return "student"
            elif obj.is_instructor:
                return "instructor"
            return {}


class TokenObtainSerializer(SimpleJWTTokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]):

        data = super().validate(attrs)

        user = self.user
        
        user_data = UserSerializer.UserRetrieveSerializer(user).data

        data['data'] = user_data
        return data