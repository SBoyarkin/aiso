from django.contrib.auth.models import User
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=255)
    inn = models.CharField(max_length=10)
    kpp = models.CharField(max_length=9)
    ogrn = models.CharField(max_length=13)
    phone = models.CharField(max_length=10)
    user = models.ManyToManyField(User, related_name='organization', blank=True)

class Certificate(models.Model):
    number = models.IntegerField()
    cn = models.CharField(max_length=100, null=True, blank=True)
    o = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    snils = models.CharField(max_length=10, null=True, blank=True)
    inn = models.CharField(max_length=10, null=True, blank=True)
    ogrn = models.CharField(max_length=15, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='certificates')
    certificate = models.FileField(upload_to='certificates')
    byte_certificate = models.BinaryField(default=None, null=True, blank=True)
    not_valid_after = models.DateTimeField()
    not_valid_before = models.DateTimeField()

# Create your models here.
