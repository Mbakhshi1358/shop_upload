from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=self.normalize_email(phone),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone , password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone= models.CharField(max_length=11, unique=True , verbose_name="شماره تلفن")
    name= models.CharField(max_length=55,verbose_name="نام", blank=True, null=True)
    lastname= models.CharField(max_length=55,verbose_name="نام خانوادگی", blank=True, null=True)
    fullname = models.CharField(max_length=55,verbose_name="نام ونام خانوادگی" , blank=True, null=True)
    email = models.EmailField(verbose_name="آدرس ایمیل",max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین؟")

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
    class Meta:
        verbose_name="حساب کاربری"
        verbose_name_plural ="حساب های کاربری"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    token = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone