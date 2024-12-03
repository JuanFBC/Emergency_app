from django.db import models

class Localidad(models.Model):
    id = models.AutoField(primary_key=True)
    localidad = models.CharField(max_length=255)


class Administrador(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    numero = models.BigIntegerField()
    correo = models.CharField(max_length=200)
    contrasena = models.CharField(max_length=255)



class Colaborador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    numero = models.BigIntegerField()
    localidad = models.CharField(max_length=255)
    estado = models.BooleanField(default=False)  # Valor predeterminado


class Emergencia(models.Model):
    id = models.AutoField(primary_key=True)
    localidad = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    fecha = models.DateField()
    act = models.BooleanField(default=True)  # Valor predeterminado
    id_administrado = models.IntegerField(default=0)  # Valor predeterminado


class Seguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    id_colaborador_id = models.IntegerField()
    id_emergencia = models.IntegerField()
    fecha_hora = models.DateTimeField()
    estado = models.BooleanField(default=False)  # Valor predeterminado


class Auditoria(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.TextField()
    pagina = models.TextField()
    fecha = models.DateTimeField()
    id_serv = models.TextField(default="N/A")  # Valor predeterminado

