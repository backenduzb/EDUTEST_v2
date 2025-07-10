from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from string import ascii_letters, digits
from random import choices
from .utils import REGION_CITY, CLASSES_CHOICE

def generate_token(length=12):
    return ''.join(choices(ascii_letters + digits, k=length))

def generate_username(first_name, last_name, length=3):
    base_username = f"{first_name.lower()}_{last_name.lower()}"
    return f"{base_username}{''.join(choices(digits, k=length))}"

def generate_password(length=8):
    return ''.join(choices(ascii_letters + digits, k=length))

REGION_CHOICE = [(viloyat, viloyat) for viloyat in REGION_CITY.keys()]
CITY_CHOICE = [(city, f"{region} viloyati - {city} tumani") for region, citylar in REGION_CITY.items() for city in citylar]

class Schools(models.Model):
    school_name = models.CharField(max_length=1024)
    region = models.CharField(max_length=256, choices=REGION_CHOICE)
    city = models.CharField(max_length=256, choices=CITY_CHOICE)
    teachers_token = models.CharField(max_length=256, unique=True, default=generate_token)

    def save(self, *args, **kwargs):
        if not self.teachers_token:
            token = generate_token()
            while Schools.objects.filter(teachers_token=token).exists():
                token = generate_token()
            self.teachers_token = token
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.school_name}"

    class Meta:
        verbose_name = "Maktab"
        verbose_name_plural = "Maktablar"

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Foydalanuvchi nomi kiritilishi shart")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_teacher', False)
        extra_fields.setdefault('is_student', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser uchun is_staff=True bo‘lishi kerak')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser uchun is_superuser=True bo‘lishi kerak')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):

    is_teacher = models.BooleanField(default=False, verbose_name="O'qituvchi")
    is_student = models.BooleanField(default=False, verbose_name="Talaba")
    school_token = models.CharField(max_length=256, blank=True, null=True)
    students_token = models.CharField(max_length=256, blank=True, null=True, default=generate_token)
    info_token = models.CharField(max_length=256, blank=True, null=True)
    student_raiting = models.IntegerField(default=0)
    class_raiting = models.IntegerField(default=0)
    school_name = models.CharField(max_length=1024, blank=True, null=True)
    class_number = models.CharField(max_length=20, choices=CLASSES_CHOICE, default="5-sinf", blank=True, null=True)
    class_letter = models.CharField(max_length=1, blank=True, null=True)
    region = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser:
            if not self.username:
                raise ValueError("Superuser uchun username kiritilishi shart")
            super().save(*args, **kwargs)
            return

        if not self.username and self.first_name and self.last_name:
            self.username = generate_username(self.first_name, self.last_name)

        if self.is_student and not self.is_teacher:
            if not self.info_token:
                raise ValueError("Talaba uchun info_token kiritilishi shart")
            
            try:
                teacher = CustomUser.objects.get(students_token=self.info_token)
                self.school_name = teacher.school_name
                self.class_letter = teacher.class_letter
                self.class_number = teacher.class_number
                self.region = teacher.region
                self.city = teacher.city
            except CustomUser.DoesNotExist:
                raise ValueError("Bunaqa ustoz yo'q.")

        if self.is_teacher and not self.is_student:
            if not self.school_token:
                raise ValueError("O'qituvchi uchun school_token kiritilishi shart")
            try:
                school = Schools.objects.get(teachers_token=self.school_token)
                self.school_name = school.school_name
                self.city = school.city
                self.region = school.region
            except Schools.DoesNotExist:
                raise ValueError("Bunaqa maktab yo'q.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'