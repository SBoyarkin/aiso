from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from mainapp.models import Organization, Certificate, MyUser
from mainapp.serializers import OrganizationSerializer, CertificateSerializer, UserSerializer
from rest_framework.response import Response

# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print(self.request.user.organization.all())

        if self.request.user.is_staff:
            return super().list(self, request, *args, **kwargs)
        else:
            queryset = self.queryset.all().intersection(self.request.user.organization.all())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)



class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

class PreviewViewSet(generics.ListAPIView):
    queryset = Certificate.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all().count()
        return Response(queryset)


