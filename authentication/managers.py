from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email must me set"))
        
        # when the admin create a staff account
        extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_active", False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_("Email must me set"))

        extra_fields.setdefault("is_student", True)
        # extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_student") is not True:
            raise ValueError(_("Student must have is_student=True"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_instructor(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email must be set"))

        extra_fields.setdefault("is_instructor", True)
        # extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_instructor") is not True:
            raise ValueError(_("Instructor must have is_instructor=True"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)