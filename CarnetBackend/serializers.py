from rest_framework import serializers
from .models import Actividad, Alumno, Asistencia, Conferencista


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = "__all__"
        depth = 1


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = "__all__"


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = "__all__"


class ConferencistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferencista
        fields = "__all__"
