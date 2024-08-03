from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .custom_permissions import *
from rest_framework_simplejwt.settings import api_settings

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token[api_settings.USER_ID_FIELD] = str(user.get_user_id())
        return token

class LoginView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            cedula = serializer.validated_data['cedula']
            password = serializer.validated_data['password']
            user = authenticate(cedula=cedula, password=password)
            print(user)
            if user is not None:
                refresh = CustomRefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

class LiderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsLiderUser]
    queryset = Lider.objects.all()
    serializer_class = LiderSerializer

    def get_queryset(self):
        if self.request.user.IsLiderUser:
            return Lider.objects.filter(user=self.request.user)

class VotanteViewSet(viewsets.ModelViewSet):
    queryset = Votante.objects.all()
    serializer_class = VotanteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.IsLiderUser:
            return Votante.objects.filter(lider__user=user)


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

class BarrioViewSet(viewsets.ModelViewSet):
    queryset = Barrio.objects.all()
    serializer_class = BarrioSerializer

class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer

class CapitanViewSet(viewsets.ModelViewSet):
    queryset = Capitan.objects.all()
    serializer_class = CapitanSerializer


class CapitanComunaViewSet(viewsets.ModelViewSet):
    queryset = CapitanComuna.objects.all()
    serializer_class = CapitanComunaSerializer

class LiderBarrioViewSet(viewsets.ModelViewSet):
    queryset = LiderBarrio.objects.all()
    serializer_class = LiderBarrioSerializer



# Se requiere hacer un sistema de información para registrar los datos de los votantes de los
# distintos municipios de Colombia.
# Allí se debe ingresar los datos básicos del votante y asignarle a éste, en que puesto de
# votación estará asignado.
# Quien ingresa los datos debe ser un usuario del sistema definido como el Rol Líder.
# El sistema debe tener un usuario administrador que podrá ver toda la información ingresada
# por los usuarios líderes.
# Los usuarios con rol Líder, únicamente pueden ver la información que ellos mismos
# registran (el sistema no permitirá que un líder pueda acceder a la información de otro líder).
# Debe quedar registrado cuando se registra un votante, y la información del usuario que lo
# registra (Log).
# Para crear un usuario líder, se debe pedir los datos básicos de identificación mínimos
# requeridos (ciudad, dirección) y una foto, para su perfil.
# Al momento de registrar un usuario (líderes y mesas de votación) en la plataforma es
# necesario obtener las coordenadas por medio del servicio de Georreferenciación de Google
# Usar base de datos relacional y/o no relacional, usted puede elegir qué datos almacena en
# una o la otra.
# Este sistema debe ser una API Rest usando JSON como método de transporte de los datos.
# Para obtener coordenadas, debe utilizarse el API de Georreferenciación de Google o
# similares.
# Tener un servicio de Login (usuario y contraseña), que permita obtener un Token para
# consumir el resto de servicios.
# El sistema deberá validar la existencia del Token en los servicios, para permitir acceder a la
# información.
# Cada servicio creado, debe tener un CRUD básico para gestionar la información.
# Exponer servicios que permitan realizar la gestión de Departamentos, Municipios, y mesas
# de votación.
# Exponer un servicio que permita obtener la cantidad total de votantes inscritos por líder.
# Exponer un servicio que permita obtener la cantidad total de votantes, en el sistema.
# Exponer un servicio que permita obtener la cantidad total de votantes inscritos por
# municipio.
# Exponer un servicio que permita obtener la cantidad total de votantes inscritos por mesa de
# votación.