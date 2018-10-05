# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Alumno(models.Model):
    class Meta:
        unique_together = (('usuario', 'no_control'),)

    usuario = models.ForeignKey(User)
    no_control = models.IntegerField()
    nombre = models.CharField(max_length=250)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return str(self.no_control)


class Conferencista(models.Model):
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=250)
    departamento = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre


class Actividad(models.Model):
    codigo_qr = models.CharField(max_length=500, primary_key=True)
    impartidor = models.ForeignKey(Conferencista)
    fecha = models.DateTimeField()
    horas = models.IntegerField()
    nombre = models.CharField(max_length=250)
    departamento = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre


class Asistencia(models.Model):
    class Meta:
        unique_together = (('alumno', 'fecha', 'actividad'),)

    alumno = models.ForeignKey(Alumno)
    fecha = models.DateTimeField()
    actividad = models.ForeignKey(Actividad)
    horas = models.IntegerField()
