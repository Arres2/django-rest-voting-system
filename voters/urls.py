from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'municipios', MunicipioViewSet)
router.register(r'comunas', ComunaViewSet)
router.register(r'barrios', BarrioViewSet)
router.register(r'puestos_votacion', PuestoViewSet)
router.register(r'capitanes', CapitanViewSet)
router.register(r'lideres', LiderViewSet)
router.register(r'capitan_comuna', CapitanComunaViewSet)
router.register(r'lider_resp_barrios', LiderBarrioViewSet)
router.register(r'datos_votantes', VotanteViewSet)


urlpatterns = [
    path('/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls