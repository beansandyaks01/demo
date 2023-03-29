from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, name=name, phone=phone)

        #Creating hashed version of the password using built-in set_password function
        user.set_password(password)
        user.save()

        #Returning the user
        return user

    def create_staff(self,email, name, phone, password=None):
        user = self.create_user(email, name, phone, password)

        user.is_staff = True
        user.save()

    def create_admin(self, email, name, password=None):
        user = self.create_admin(email, name, password)

        user.is_admin = True
        user.is_staff = True

        user.save()


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    phone=models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_phone_name(self):
        return self.phone
    def __str__(self):
        return self.email