from django.contrib.auth.models import AbstractUser
from django.db import models

class HistoryAtributes(models.Model):
    pass

class MyUser(AbstractUser):
    snils = models.CharField(max_length=20)

class Organization(models.Model):
    name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=255)
    inn = models.CharField(max_length=10)
    kpp = models.CharField(max_length=9)
    ogrn = models.CharField(max_length=13)
    phone = models.CharField(max_length=10)
    user = models.ManyToManyField(MyUser, related_name='organization', blank=True)

class Certificate(models.Model):
    serial_number = models.CharField(max_length=150, unique=True)
    cn = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)
    sur_name = models.CharField(max_length=100, null=True, blank=True)
    o = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    snils = models.CharField(max_length=10)
    inn = models.CharField(max_length=10)
    ogrn = models.CharField(max_length=15, null=True, blank=True)
    owner = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE, related_name='certificates')
    certificate = models.FileField(upload_to='certificates')
    byte_certificate = models.BinaryField(default=None, null=True, blank=True)
    not_valid_after = models.DateTimeField()
    not_valid_before = models.DateTimeField()

# Create your models here.
