from rest_framework.exceptions import ValidationError, NotFound

from mainapp.models import MyUser
from rest_framework import serializers, status
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from mainapp.models import Organization, Certificate



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'fullname', 'inn', 'kpp', 'ogrn', 'phone', 'user']
        read_only_fields = ['user']


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'cn', 'o', 'email', 'snils', 'owner', 'ogrn', 'serial_number', 'certificate',
                  'byte_certificate', 'not_valid_after', 'not_valid_before']
        read_only_fields = ['serial_number', 'cn', 'o', 'email', 'snils', 'inn', 'ogrn',
                            'owner', 'not_valid_after', 'not_valid_before']

    def create(self, validated_data):
        cert = validated_data.pop('certificate')
        data = cert.read()
        decode_data = x509.load_der_x509_certificate(data, default_backend())
        subject = decode_data.subject
        print(subject)
        all_attr = {}
        for attribute in subject:
            all_attr[attribute.rfc4514_attribute_name.lower()] = attribute.value

        if Certificate.objects.filter(serial_number=decode_data.serial_number).exists():
            raise ValidationError('Certificate already exists', status.HTTP_403_FORBIDDEN)
        else:
            ogrn = all_attr.get('1.2.643.100.1')
            snils = all_attr.get('1.2.643.100.3')
            inn = all_attr.get('1.2.643.3.131.1.1')
            email = all_attr.get('1.2.840.113549.1.9.1')
            username = email.split('@')[0]
            sur_name = all_attr.get('2.5.4.4')
            given_name = all_attr.get('2.5.4.42')
            o = all_attr.get('o')
            validated_data['sur_name'] = sur_name
            validated_data['given_name'] = given_name
            validated_data['ogrn'] = ogrn
            validated_data['snils'] = snils
            validated_data['inn'] = inn
            validated_data['email'] = email
            validated_data['o'] = o
            validated_data['cn'] = all_attr.get('cn')
            validated_data['not_valid_after'] = decode_data.not_valid_after_utc
            validated_data['not_valid_before'] = decode_data.not_valid_before_utc
            validated_data['serial_number'] = decode_data.serial_number
            validated_data['byte_certificate'] = data
        if validated_data.get('ogrn'):
            Organization.objects.get_or_create(name=all_attr.get('o'), defaults={'ogrn': ogrn})
        else:
            org = Organization.objects.get(name=all_attr.get('o'))
            if org:
                user, created = MyUser.objects.get_or_create(
                    snils=snils,
                    defaults={'email': email, 'username': username}
                )
                validated_data['owner'] = user
                user.organization.add(org)
            else:
                raise NotFound('Organization not found')
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields =  '__all__'
