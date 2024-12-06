from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from mainapp.models import Organization, Certificate, MyUser
from mainapp.serializers import OrganizationSerializer, CertificateSerializer, UserSerializer
from rest_framework.response import Response

# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

class PreviewViewSet(generics.ListAPIView):
    queryset = Certificate.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all().count()
        return Response(queryset)


