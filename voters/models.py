from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('The Cedula field must be set')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cedula, password, **extra_fields)

class Capitan(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    nombre= models.CharField(("nombre"), max_length=50)
    apellido= models.CharField(("apellido"), max_length=50)
    telefono = models.IntegerField()

class CustomUser(AbstractUser):
    is_lider = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    cedula = models.IntegerField(unique=True, primary_key=True)
    direccion = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return str(self.cedula)  # Ensure this returns a string
    
    def get_user_id(self):
        return self.cedula


class Lider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    capitan = models.ForeignKey(Capitan, verbose_name=("capitan"), on_delete=models.CASCADE)
    # Add any additional fields specific to Lider
    class Meta:
        verbose_name = 'lider'
        verbose_name_plural = 'lideres'

class Municipio(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    nombre= models.CharField(("nombre"), max_length=50)

class Comuna(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    nombre= models.CharField(("nombre"), max_length=50)
    municipio = models.ForeignKey(Municipio, verbose_name=("municipio"), on_delete=models.CASCADE)

class Barrio(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    nombre= models.CharField(("nombre"), max_length=50)
    comuna = models.ForeignKey(Comuna, verbose_name=("comuna"), on_delete=models.CASCADE)

class Puesto(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    direccion = models.CharField(max_length=100)
    nombre= models.CharField(("nombre"), max_length=50)
    municipio = models.ForeignKey(Municipio, verbose_name=("municipio"), on_delete=models.CASCADE)

class Votante(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lider = models.ForeignKey(Lider, verbose_name=("lider"), on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puesto, verbose_name=("puesto"), on_delete=models.CASCADE)
    barrio =  models.ForeignKey(Barrio, verbose_name=("barrio"), on_delete=models.CASCADE)
    mesa = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'votante'
        verbose_name_plural = 'votantes'

class LiderBarrio(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    lider = models.ForeignKey(Lider, verbose_name=("lider"), on_delete=models.CASCADE)
    capitan= models.ForeignKey(Capitan, verbose_name=("capitan"), on_delete=models.CASCADE)
    barrio = models.ForeignKey(Barrio, verbose_name=("barrio"), on_delete=models.CASCADE)

class CapitanComuna(models.Model):
    id= models.UUIDField(primary_key=True, unique=True, editable = False, default=uuid.uuid4)
    comuna = models.ForeignKey(Comuna, verbose_name=("comuna"), on_delete=models.CASCADE)
    capitan= models.ForeignKey(Capitan, verbose_name=("capitan"), on_delete=models.CASCADE)




