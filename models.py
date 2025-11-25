from django.db import models


class PadreMadre(models.Model):
    id_padre_madre = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono_principal = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    dni = models.CharField(max_length=20)
    relacion_con_nino = models.CharField(max_length=50)
    profesion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class GrupoNinos(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=50, unique=True)
    edad_minima = models.IntegerField()
    edad_maxima = models.IntegerField()
    id_personal_cargo = models.ForeignKey(
        'PersonalGuarderia',
        on_delete=models.SET_NULL,
        null=True
    )
    num_ninos_actual = models.IntegerField()
    capacidad_maxima = models.IntegerField()
    descripcion_actividades = models.TextField()

    def __str__(self):
        return self.nombre_grupo


class PersonalGuarderia(models.Model):
    id_personal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    dni = models.CharField(max_length=20)
    certificaciones = models.TextField()
    turno = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Nino(models.Model):
    id_nino = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    id_padre_madre_principal = models.ForeignKey(
        PadreMadre,
        on_delete=models.CASCADE
    )
    alergias = models.TextField(null=True, blank=True)
    necesidades_especiales = models.TextField(null=True, blank=True)

    # Relación especial hacia nombre_grupo (unique)
    grupo_asignado = models.ForeignKey(
        GrupoNinos,
        to_field='nombre_grupo',
        db_column='grupo_asignado',
        on_delete=models.SET_NULL,
        null=True
    )

    fecha_inscripcion = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ActividadGuarderia(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre_actividad = models.CharField(max_length=100)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)
    duracion_minutos = models.IntegerField()
    id_grupo = models.ForeignKey(
        GrupoNinos,
        on_delete=models.CASCADE
    )
    material_requerido = models.TextField()
    es_obligatoria = models.BooleanField()

    def __str__(self):
        return self.nombre_actividad


class AsistenciaNino(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_nino = models.ForeignKey(Nino, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    estuvo_enfermo = models.BooleanField()
    notas_dia = models.TextField(null=True, blank=True)
    id_personal_registro = models.ForeignKey(PersonalGuarderia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Asistencia {self.id_asistencia} - Niño {self.id_nino_id}"


class PagoMensualidad(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_nino = models.ForeignKey(Nino, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=50)
    mes_correspondiente = models.DateField()
    estado_pago = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return f"Pago {self.id_pago} - Niño {self.id_nino_id}"

