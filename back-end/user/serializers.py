from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CharField

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])
    password2 = CharField(write_only=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone_number', 'image',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': _("Password fields didn't match."),
                'password2': _("Password fields didn't match"),
            })

        return attrs

    def create(self, validated_data) -> 'User':
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
