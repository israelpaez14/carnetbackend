# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Actividad, Alumno, Asistencia, Conferencista
from django.contrib import admin

# Register your models here.
admin.site.register(Asistencia)
admin.site.register(Alumno)
admin.site.register(Actividad)
admin.site.register(Conferencista)
