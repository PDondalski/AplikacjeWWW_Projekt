from rest_framework import serializers
from .models import BgBudzet, BgKategoria, BgWydatek, BgOszczednosc
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate



class BgBudzetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = BgBudzet
        fields = ['id','budzet_rok', 'budzet_miesiac', 'owner', 'budzet_wartosc']
        read_only_fields = ['id']
class BgKategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgKategoria
        fields = ['id', 'budzet', 'kategoria_nazwa', 'kategoria_wydatek']
        read_only_fields = ['id']
class BgWydatekSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgWydatek
        fields = ['wydatek_budzet', 'wydatek_kategoria', 'wydatek_wartosc', 'wydatek_data']
        read_only_fields = ['id']
class BgOszczednoscSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgOszczednosc
        fields = ['budzet', 'osczednosc_calkowita']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
            'email', 'first_name', 'last_name')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs