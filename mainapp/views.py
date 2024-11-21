from django.shortcuts import render
from rest_framework import viewsets

from mainapp.models import Organization, Certificate, MyUser
from mainapp.serializers import OrganizationSerializer, CertificateSerializer, UserSerializer


# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer