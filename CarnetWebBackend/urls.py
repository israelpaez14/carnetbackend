from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from CarnetBackend.views import ActividadViewset, ConferencistaViewset, AsistenciaViewset, registrarConferencista, \
    registrarAlumno, registrarAsistencia, loggin_alumnos, logout_view, loggin_expositores, login_superusuarios, \
    administrador_dashboard, login_form_super, expositor_dashboard, login_form_expositor, registrar_actividad, index

router = DefaultRouter()
router.register("actividades", ActividadViewset)
router.register("conferencistas", ConferencistaViewset)
router.register("asistencias", AsistenciaViewset)

urlpatterns = [
    url(r'^index', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url("", include(router.urls)),
    url('api-auth/', include("rest_framework.urls")),
    url(r'^registrarConferencista/', registrarConferencista),
    url(r'^registrarAlumno/', registrarAlumno),
    url(r'^iniciar_sesion_admin/', login_form_super, name='login_form_super'),
    url(r'^iniciar_sesion_expositor/', login_form_expositor, name='login_form_expositor'),
    url(r'^registrarAsistencia/', registrarAsistencia),
    url(r'^loggin_alumnos/', loggin_alumnos, name='login_alumnos'),
    url(r'^loggin_expositores/', loggin_expositores, name='login_expositores'),
    url(r'^login_superusuarios/', login_superusuarios, name='login_superusuarios'),
    url(r'^administrador_dashboard/', administrador_dashboard, name='administrador_dashboard'),
    url(r'^expositor_dashboard/', expositor_dashboard, name='expositor_dashboard'),
    url(r'^registrar_actividad/', registrar_actividad, name='registrar_actividad'),
    url(r'^logout/', logout_view, name='logout'),

]
