# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-28 01:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('codigo_qr', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('horas', models.IntegerField()),
                ('nombre', models.CharField(max_length=250)),
                ('departamento', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_control', models.IntegerField()),
                ('nombre', models.CharField(max_length=250)),
                ('carrera', models.CharField(max_length=100)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('horas', models.IntegerField()),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarnetBackend.Actividad')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarnetBackend.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Conferencista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('departamento', models.CharField(max_length=250)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='actividad',
            name='impartidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarnetBackend.Conferencista'),
        ),
        migrations.AlterUniqueTogether(
            name='asistencia',
            unique_together=set([('alumno', 'fecha', 'actividad')]),
        ),
        migrations.AlterUniqueTogether(
            name='alumno',
            unique_together=set([('usuario', 'no_control')]),
        ),
    ]
