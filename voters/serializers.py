from rest_framework import serializers
from .models import  Municipio, Comuna, Barrio, Puesto, Capitan, Lider, CapitanComuna, LiderBarrio, Votante, CustomUser

class LoginSerializer(serializers.Serializer):
    cedula = serializers.IntegerField()
    password = serializers.CharField()

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        # fields = ['id_municipio', 'nombre']
        fields="_all_"
        depth = 1  

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        # fields = ['id_comuna', 'nombre', 'municipio']
        fields="_all_"

class BarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrio
        # fields = ['id_barrio', 'nombre', 'comuna']
        fields="_all_"

class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto
        # fields = ['id_puesto', 'nombre', 'direccion', 'municipio']
        fields="_all_"

class CapitanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitan
        # fields = ['id_capitan', 'nombres', 'apellidos', 'celular']
        fields="_all_"

# class LiderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lider
#         fields = ['id_lider', 'nombres', 'apellidos', 'celular', 'capitan']
#         fields="_all_"

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['cedula', 'username', 'password', 'is_lider', 'is_admin', 'direccion', 'foto', 'telefono']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LiderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Lider
        fields = ['id', 'user']


class CapitanComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitanComuna
        # fields = ['id_capitancomuna', 'comuna', 'capitan']
        fields="_all_"

class LiderBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiderBarrio
        # fields = ['id_liderresponsable', 'lider', 'capitancomuna', 'barrio']
        fields="_all_"

class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        # fields="_all_"
        fields = ["first_name", "last_name", 'direccion', 'telefono', 'cedula', 'lider', 'barrio', 'puesto', 'mesa']
        extra_kwargs = {"password":{"write_only":True}}

        def validate_cedula(self, value):
        # Custom validation for cedula
            if not value.isdigit() or len(value) != 10:
                raise serializers.ValidationError("Cédula must be a 10-digit number")
            return value
        