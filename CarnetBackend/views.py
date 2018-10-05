# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from CarnetBackend.permisos import IsOwnerPermission, IsSelf, IsOwnAsistencia
from .models import Alumno, Asistencia, Actividad, Conferencista
from .serializers import AlumnoSerializer, AsistenciaSerializer, ActividadSerializer, ConferencistaSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group

import random


# Create your views here.
def get_codigo_aleatorio():
    cadena = ""
    for i in range(20):
        cadena = cadena + str(chr(random.randint(65, 90))) + str(random.randint(0, 9))
    return cadena


class AsistenciaViewset(viewsets.ModelViewSet):
    serializer_class = AsistenciaSerializer
    queryset = Asistencia.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnAsistencia)

    def list(self, request, *args, **kwargs):
        asistencias = self.queryset.filter(alumno=Alumno.objects.get(usuario=request.user))
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


def registrarAsistencia(request):
    try:
        if request.user.is_anonymous:
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)
        print(request.user)
        if not Alumno.objects.filter(usuario=request.user).exists():
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)
        codigo = request.POST["codigo_qr"]

        if codigo == '':
            return HttpResponse("Codigo Invalido", status=status.HTTP_400_BAD_REQUEST)
        if not Actividad.objects.filter(codigo_qr=codigo).exists():
            return HttpResponse("Codigo Invalido", status=status.HTTP_400_BAD_REQUEST)

        actividad = Actividad.objects.get(codigo_qr=codigo)
        alumno = Alumno.objects.get(usuario=request.user)
        asistencia = Asistencia()

        if Asistencia.objects.filter(actividad=actividad, alumno=alumno).exists():
            return HttpResponse("Codigo ya consumido", status=status.HTTP_400_BAD_REQUEST)

        asistencia.horas = actividad.horas
        asistencia.actividad = actividad
        asistencia.fecha = actividad.fecha
        asistencia.alumno = alumno
        asistencia.save()
        return HttpResponse("Ok", status=status.HTTP_200_OK)
    except Exception as e:
        print(e.message)
        print(e.args)
        return HttpResponse("Error", status=status.HTTP_400_BAD_REQUEST)


class ActividadViewset(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    queryset = Actividad.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerPermission)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            actividades = self.queryset
        else:
            actividades = self.queryset.filter(impartidor=Conferencista.objects.get(usuario=request.user))
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ActividadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            codigo = get_codigo_aleatorio()
            while Actividad.objects.filter(codigo_qr=codigo).exists():
                codigo = get_codigo_aleatorio()
            serializer.save(impartidor=Conferencista.objects.get(usuario=request.user), codigo_qr=codigo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        actividad = get_object_or_404(self.queryset, codigo_qr=pk)
        asistencias = actividad.asistencia_set.all()
        asistentes = []
        for asistencia in asistencias:
            asistentes.append(asistencia.alumno)
        alumno_serializer = AlumnoSerializer(asistentes, many=True)
        serializer = ActividadSerializer(actividad)
        return Response({"datos_actividad": serializer.data, "asistentes": alumno_serializer.data})


class ConferencistaViewset(viewsets.ModelViewSet):
    queryset = Conferencista.objects.all()
    serializer_class = ConferencistaSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsSelf,)


def registrarConferencista(request):
    try:
        if request.user is None:
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)

        if not request.user.is_superuser:
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)
        nombre = request.POST["nombre"]
        departamento = request.POST["departamento"]
        nombreusuario = request.POST["nombreusuario"]
        password = request.POST["password"]
        if password == '' or nombreusuario == '' or departamento == '' or nombre == '':
            return HttpResponse("Campos invalidos", status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=nombreusuario).exists():
            return HttpResponse("El usuario ya existe", status=status.HTTP_400_BAD_REQUEST)

        usuario = User.objects.create_user(username=nombreusuario, password=password, email='')
        grupo_maestros = Group.objects.get(name="Maestros")
        usuario.save()
        usuario.groups.add(grupo_maestros)
        conferencista_obj = Conferencista()
        conferencista_obj.nombre = nombre
        conferencista_obj.departamento = departamento
        conferencista_obj.usuario = usuario
        conferencista_obj.save()
        return HttpResponse("Ok", status=status.HTTP_200_OK)
    except Exception as e:
        print(e.message)
        print(e.args)
        return HttpResponse("Error", status=status.HTTP_400_BAD_REQUEST)


def registrarAlumno(request):
    try:
        if request.user is None:
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)

        if not request.user.is_superuser:
            return HttpResponse("No permitido", status=status.HTTP_403_FORBIDDEN)
        nombre = request.POST["nombre"]
        carrera = request.POST["carrera"]
        no_control = request.POST["no_control"]
        password = request.POST["password"]
        nombreusuario = request.POST["no_control"]
        if password == '' or nombreusuario == '' or carrera == '' or nombre == '':
            return HttpResponse("Campos invalidos", status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=nombreusuario).exists():
            return HttpResponse("Ya existe un alumno con ese usuario", status=status.HTTP_400_BAD_REQUEST)

        usuario = User.objects.create_user(username=nombreusuario, password=password, email='')
        grupo_alumnos = Group.objects.get(name="Alumnos")
        usuario.save()
        usuario.groups.add(grupo_alumnos)
        alumno_obj = Alumno()
        alumno_obj.nombre = nombre
        alumno_obj.carrera = carrera
        alumno_obj.usuario = usuario
        alumno_obj.no_control = no_control
        alumno_obj.save()
        return HttpResponse("Ok", status=status.HTTP_200_OK)
    except Exception as e:
        print(e.message)
        print(e.args)
        return HttpResponse("Error", status=status.HTTP_400_BAD_REQUEST)


def login_form_super(request):
    return render(request, "login.html", {})


def login_form_expositor(request):
    return render(request, "login_expositores.html", {})


def loggin_alumnos(request):
    try:
        usuario = request.POST['usuario']
        password = request.POST['password']
        print(usuario)
        print(password)
        user = authenticate(username=usuario, password=password)
        if user is None:
            return HttpResponse("Credenciales incorrectas", status=status.HTTP_404_NOT_FOUND)

        if not user.groups.filter(name="Alumnos").exists():
            return HttpResponse("Credenciales incorrectas", status=status.HTTP_404_NOT_FOUND)

        login(request, user)
        return HttpResponse("Login exitoso", status=status.HTTP_202_ACCEPTED)

    except Exception  as e:
        print(e.message)
        return HttpResponse("Error", status=status.HTTP_404_NOT_FOUND)


def loggin_expositores(request):
    try:
        usuario = request.POST['usuario']
        password = request.POST['password']
        print(usuario)
        print(password)
        user = authenticate(username=usuario, password=password)
        if user is None:
            return render(request, "login_expositores.html", {"error": "Credenciales incorrectas"})

        if not user.groups.filter(name="Maestros").exists():
            return render(request, "login_expositores.html", {"error": "Credenciales incorrectas"})

        login(request, user)
        return redirect(to='expositor_dashboard')

    except Exception  as e:
        print(e.message)
        return redirect(to='logout')


def login_superusuarios(request):
    try:
        usuario = request.POST['usuario']
        password = request.POST['password']
        print(usuario)
        print(password)
        user = authenticate(username=usuario, password=password)
        if user is None or not user.is_superuser:
            return render(request, "login.html", {"error": "Credenciales incorrectas"})

        login(request, user)
        return redirect(to="administrador_dashboard")

    except Exception  as e:
        print(e.message)
        return render(request, "login.html", {"error": "Error del servidor, contacte al administrador del sistema"})


@login_required(login_url='/iniciar_sesion_admin/')
def logout_view(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(to='login_form_super')
    elif request.user.groups.filter(name='Maestros').exists():
        logout(request)
        return redirect(to='login_form_expositor')
    else:
        return HttpResponse("Logout exitoso", status=status.HTTP_202_ACCEPTED)


@login_required(login_url='/iniciar_sesion_admin/')
def administrador_dashboard(request):
    if not request.user.is_superuser:
        return redirect(to="logout")
    return render(request, "dashboard.html", {"nombre": request.user})


@login_required(login_url='/iniciar_sesion_expositor/')
def expositor_dashboard(request):
    if not request.user.groups.filter(name='Maestros').exists():
        return redirect(to="logout")
    return render(request, "dashboard_expositor.html", {"nombre": request.user})


@login_required(login_url='/iniciar_sesion_expositor/')
def registrar_actividad(request):
    if not request.user.groups.filter(name='Maestros').exists():
        return redirect(to="logout")
    return render(request, 'registrar_actividad.html', {"nombre": request.user})


def index(request):
    return render(request, "index.html", {})
