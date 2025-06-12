from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='patient', **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role of Admin.')
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
        ('lab_staff', 'Lab Staff'),
        ('pharmacist', 'Pharmacist'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # 🔥 THÊM 2 dòng này:
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

