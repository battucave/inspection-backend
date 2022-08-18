from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import datetime

JOB_ROLES = [
    ("owner", "owner"),
    ("maintenance", "maintenance"),
    ("vendor", "vendor"),
    
]


VERIFICATION_EXPIRY=15


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email',max_length=255,blank=True,unique=True)
    phone = models.CharField(null=True,max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=100, choices=JOB_ROLES, null=True)
    is_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None

    def __str__(self):
        return self.email
    
    def is_vendor(self):
        if self.id:
            return self.user_type == 'vendor'
        return False
    
    def is_owner(self):
        if self.id:
            return self.user_type == 'owner'
        return False

    def is_maintenance(self):
        if self.id:
            return self.user_type == 'maintenance'
        return False
    
        


class VerificationCode(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(minutes=VERIFICATION_EXPIRY))

    def save(self, *args, **kwargs):
        self.code = "".join([str(random.randint(0,9)) for i in range(4)])
        super(VerificationCode, self).save(*args, **kwargs)
    
    def expired(self):
        return datetime.datetime.now()>=self.expiry
    
    

