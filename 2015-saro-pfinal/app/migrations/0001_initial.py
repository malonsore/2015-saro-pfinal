# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=500)),
                ('gratuito', models.CharField(max_length=500)),
                ('fecha', models.CharField(max_length=500)),
                ('fechafin', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500)),
                ('tipo', models.CharField(max_length=500)),
                ('duracion', models.CharField(max_length=500)),
                ('precio', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=200)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('background', models.CharField(max_length=200)),
                ('fuente', models.CharField(max_length=200)),
                ('letra', models.CharField(max_length=200)),
                ('amigos', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('incidencias', models.ManyToManyField(to='app.Tipos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuarios_tipos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('elegidaen', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
