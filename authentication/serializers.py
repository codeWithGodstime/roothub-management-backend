from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as SimpleJWTTokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from faker import Faker
from decimal import Decimal

from .models import Program, Student, Instructor, StudentPayment, InstructorSkill

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
            user = User.objects.create_user(
                password=self.context.get("generated_password"), **validated_data)
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
                "role",
                "next_of_kin_contact",
                "next_of_kin_name",
                "next_of_kin_email",
                "next_of_kin_relationship",
                "home_address"
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

    class ResetPasswordRequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)

    class ChangePasswordSerializer(serializers.Serializer):
        token = serializers.CharField(required=True)
        new_password = serializers.CharField(write_only=True, required=True)

        def validate_new_password(self, value):
            from django.contrib.auth.password_validation import validate_password
            validate_password(value)
            return value

        def validate(self, data):
            token = data.get("token")
            new_password = data.get("new_password")

            # Decode user ID from the token
            try:
                user_id, token = token.split(":", 1)
                
                user = User.objects.get(id=user_id)
            except (ValueError, User.DoesNotExist):
                raise serializers.ValidationError({"token": "Invalid token."})

            # Validate the token
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                raise serializers.ValidationError(
                    {"token": "Invalid or expired token."})

            self.user = user
            return data

        def save(self):
            """
            Updates the user's password.
            """
            self.user.set_password(self.validated_data["new_password"])
            self.user.save()


class StudentPaymentSerializer:
    class StudentPaymentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = StudentPayment
            fields = ["payment_date", "amount"]

    class StudentPaymentRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = StudentPayment
            fields = ["id", "student", "payment_date",
                      "amount", "created_at", "updated_at"]


class StudentSerializer:
    class StudentCreateSerializer(serializers.ModelSerializer):
        user = UserSerializer.UserCreateSerializer()
        payment = StudentPaymentSerializer.StudentPaymentCreateSerializer()

        class Meta:
            model = Student
            fields = (
                "user",
                "program",
                "type",
                "payment_plan",
                "payment"
            )

        def create(self, validated_data):

            # extract payment
            payment = validated_data.pop("payment")

            # extract user data
            if "user" in validated_data:
                user = validated_data.pop('user')
                # create user
                user = User.objects.create_student(
                    password=self.context.get("generated_password"), **user
                )
                user.save()

            student = Student.objects.create(user=user, **validated_data)
            student.save()

            if "payment" in validated_data:
                payment_data = StudentPayment.objects.create(**payment)
                payment_data.save()

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


class InstructorSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorSkill
        fields = ["name", "is_primary"]


class InstructorSerializer(serializers.ModelSerializer):

    class InstructorCreateSerializer(serializers.ModelSerializer):
        user = UserSerializer.UserCreateSerializer()
        skills = InstructorSkillSerializer(many=True)

        class Meta:
            model = Instructor
            fields = ("user", "skills", "account_number",
                      "account_name", "bank_name")

        def create(self, validated_data):
            if "skills" in validated_data:
                skills_data = validated_data.pop("skills")

            # extract user data
            if "user" in validated_data:
                user = validated_data.pop('user')
                # create user
                user = User.objects.create_instructor(
                    password=self.context.get("generated_password"), **user)
                user.save()

            instructor = Instructor.objects.create(user=user, **validated_data)
            instructor.save()

            skill_instances = [
                InstructorSkill(instructor=instructor, **skill_data)
                for skill_data in skills_data
            ]
            InstructorSkill.objects.bulk_create(skill_instances)

            return instructor

    class InstructorRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = Instructor
            fields = "__all__"


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
            # Convert `Decimal` to `float` for specific fields
            if "total_amount" in data and isinstance(data["total_amount"], Decimal):
                data["total_amount"] = float(data["total_amount"])

            return data

    class ProgramUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Program
            fields = ['name', "duration", "total_amount"]

        def to_representation(self, instance):
            """
            Customize the serialized output to convert Decimal fields to float.
            """
            data = super().to_representation(instance)
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
