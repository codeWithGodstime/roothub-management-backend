from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer
from faker import Faker
from decimal import Decimal

# from .models import User, Student, Instructor
from .models import Program, Student
from utils.util_functions import generate_passwords

User = get_user_model()
faker = Faker()


class UserSerializer:
    class UserCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "email",
                "first_name",
                "last_name",
                "next_of_kin_contact",
                "next_of_kin_name",
                "next_of_kin_email",
                "next_of_kin_relationship",
                "home_address"
            )

        def validate(self, attrs):
            return super().validate(attrs)

        def create(self, validated_data):
            generated_password = generate_passwords()
            user = User.objects.create_user(
                password=generated_password, **validated_data)

            message = f"""
            Your account details are
            password: {generated_password}
            """
            user.email_user("Roothub Account Login Credentials",
                            message, "admin@developer.com")
            user.save()
            return user

    class UserRetrieveSerializer(serializers.ModelSerializer):

        role = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = (
                "email",
                "first_name",
                "last_name",
                "id",
                "role"
            )

        def get_role(self, obj) -> str:
            if obj.is_student:
                return "student"
            elif obj.is_instructor:
                return "instructor"
            elif obj.is_superuser:
                return "admin"
            elif obj.is_staff:
                return "staff"

            return None


class StudentSerializer:
    class StudentCreateSerializer(serializers.ModelSerializer):
        user = UserSerializer.UserCreateSerializer()

        class Meta:
            model = Student
            fields = (
                "user",
                "program",
                "type",
                "payment_plan",
            )

        def create(self, validated_data):

            # extract user data
            if "user" in validated_data:
                user = validated_data.pop('user')
                # create user
                generated_password = generate_passwords()
                user = User.objects.create_student(
                    password=generated_password, **user
                )
        
                message = f"""
                Your account details are
                password: {generated_password}
                """
                user.email_user("Roothub Account Login Credentials",
                                message, "admin@developer.com")
                user.save()

            student = Student.objects.create(user=user, **validated_data)
            student.save()
            return student

    class StudentRetrieveSerializer(serializers.ModelSerializer):
        user = UserSerializer.UserRetrieveSerializer()

        class Meta:
            model = Student
            fields = (
                "id",
                "user",
                "program",
                "type",
                "created_at",
                "updated_at",
                "payment_plan"
            )


# class InstructorSerializer(serializers.ModelSerializer):

#     class InstructorCreateSerializer(serializers.ModelSerializer):
#             user = UserSerializer.UserCreateSerializer()

#             class Meta:
#                 model = Instructor
#                 fields = ("user", )

#             def create(self, validated_data):

#                 # extract user data
#                 if "user" in validated_data:
#                     user = validated_data.pop('user')
#                     #create user
#                     generated_password = generate_passwords()
#                     user = User.objects.create_instructor(password=generated_password, **user)

#                     message = f"""
#                     Your account details are
#                     password: {generated_password}
#                     """
#                     user.email_user("Roothub Account Login Credentials", message, "admin@developer.com")
#                     user.save()

#                 instructor = Instructor.objects.create(user = user, **validated_data)
#                 instructor.save()

#                 return instructor

#     class InstructorRetrieveSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Instructor
#             fields = "__all__"


class ProgramSerializer:
    class ProgramCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Program
            fields = ("name", "duration", "total_amount")

    class ProgramRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = Program
            fields = "__all__"

        def to_representation(self, instance):
            """
            Customize the serialized output to convert Decimal fields to float.
            """
            data = super().to_representation(instance)
            print(data, "representation")
            # Convert `Decimal` to `float` for specific fields
            if "total_amount" in data and isinstance(data["total_amount"], Decimal):
                data["total_amount"] = float(data["total_amount"])

            return data


class TokenObtainSerializer(SimpleJWTTokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]):

        data = super().validate(attrs)

        user = self.user

        user_data = UserSerializer.UserRetrieveSerializer(user).data

        data['data'] = user_data
        return data
