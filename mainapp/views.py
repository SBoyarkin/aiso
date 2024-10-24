from django.shortcuts import render
from rest_framework import viewsets

from mainapp.models import Organization, Certificate
from mainapp.serializers import OrganizationSerializer, CertificateSerializer


# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer