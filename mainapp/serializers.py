from pprint import pprint

from cryptography.hazmat.primitives import hashes
from rest_framework import serializers
from rest_framework.response import Response
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from mainapp.models import Organization, Certificate


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'fullname','inn','kpp','ogrn','phone','user']
        read_only_fields = ['user']


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['cn','o','email','snils','owner','ogrn','number','certificate', 'byte_certificate', 'not_valid_after', 'not_valid_before']
        read_only_fields = ['cn','o','email','snils','inn','ogrn','owner','not_valid_after', 'not_valid_before']

    def create(self, validated_data):
        cert = validated_data.pop('certificate')
        data = cert.read()
        decode_data = x509.load_der_x509_certificate(data, default_backend())
        subject = decode_data.subject
        all_attr = {}
        for attribute in subject:
            all_attr[attribute.rfc4514_attribute_name.lower()] = attribute.value

        # pprint(all_attr)
        validated_data['ogrn'] = all_attr.get('1.2.643.100.1')
        validated_data['snils'] = all_attr.get('1.2.643.100.3')
        validated_data['inn'] = all_attr.get('1.2.643.3.131.1.1')
        validated_data['email'] = all_attr.get('1.2.840.113549.1.9.1')
        validated_data['o'] = all_attr.get('o')
        validated_data['cn'] = all_attr.get('cn')
        validated_data['not_valid_after'] = decode_data.not_valid_after_utc
        validated_data['not_valid_before'] = decode_data.not_valid_before_utc


        return super().create(validated_data)


