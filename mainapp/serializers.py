from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.fields import SerializerMethodField

from mainapp.models import MyUser
from rest_framework import serializers, status
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from mainapp.models import Organization, Certificate


def get_username(given_name, sur_name):
    result = ''
    name = given_name.split(' ')
    login = f'{name[0][0]}{name[1][0]}{sur_name}'.lower()
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', '-': '-'
    }

    for i in login:
        tl = transliteration_dict.get(i)
        result += tl if tl is not None else ''
    return result



class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'cn', 'o', 'email', 'snils', 'owner', 'ogrn', 'serial_number', 'certificate',
                   'not_valid_after', 'not_valid_before']
        read_only_fields = ['serial_number', 'cn', 'o', 'email', 'snils', 'inn', 'ogrn',
                            'owner', 'not_valid_after', 'not_valid_before']

    def create(self, validated_data):
        cert = validated_data.get('certificate')
        data = cert.read()
        decode_data = x509.load_der_x509_certificate(data, default_backend())
        subject = decode_data.subject
        # print(subject)
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
            sur_name = all_attr.get('2.5.4.4')
            given_name = all_attr.get('2.5.4.42')
            last_name = all_attr.get('2.5.4.42').split(' ')[0]
            middle_name = all_attr.get('2.5.4.42').split(' ')[1:]
            middle_name = ' '.join(middle_name)
            username = get_username(given_name, sur_name)
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
            # print(validated_data)
        if validated_data.get('ogrn'):
            Organization.objects.get_or_create(name=all_attr.get('o'), defaults={'ogrn': ogrn})
        else:
            try:
                org = Organization.objects.get(name=all_attr.get('o'))
            except ObjectDoesNotExist:
                raise ValidationError('Organization does not exist', status.HTTP_404_NOT_FOUND)

            if org:
                user, created = MyUser.objects.get_or_create(
                    snils=snils,
                    defaults={'email': email, 'username': username,
                              'first_name': sur_name, 'last_name': last_name,
                              'middle_name': middle_name}
                )
                validated_data['owner'] = user
                user.organization.add(org)
            else:
                raise NotFound('Organization not found')
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True, read_only=True)
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'snils', 'first_name', 'last_name', 'certificates']

class OrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'fullname', 'inn', 'kpp', 'ogrn', 'phone', 'user']
        read_only_fields = ['user']

