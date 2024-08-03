from django.contrib import admin
from .models import Capitan, CustomUser, Lider, Municipio, Comuna, Barrio, Puesto, Votante, LiderBarrio, CapitanComuna

admin.site.register(Capitan)
admin.site.register(CustomUser)
admin.site.register(Lider)
admin.site.register(Municipio)
admin.site.register(Comuna)
admin.site.register(Barrio)
admin.site.register(Puesto)
admin.site.register(Votante)
admin.site.register(LiderBarrio)
admin.site.register(CapitanComuna)