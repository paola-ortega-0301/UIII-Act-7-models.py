from django.db import models

# ------------------------------------------------------
# Cliente
# ------------------------------------------------------
class ClienteLavanderia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    direccion_recogida = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    fecha_registro = models.DateField()
    notas_cliente = models.TextField(null=True, blank=True)
    preferencias_lavado = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ------------------------------------------------------
# Empleado
# ------------------------------------------------------
class EmpleadoLavanderia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    turno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"


# ------------------------------------------------------
# Artículo de Ropa
# ------------------------------------------------------
class ArticuloRopa(models.Model):
    tipo_prenda = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    tamano = models.CharField(max_length=20)
    instrucciones_especiales = models.TextField(null=True, blank=True)
    costo_lavado_estandar = models.DecimalField(max_digits=5, decimal_places=2)
    estado_articulo = models.CharField(max_length=50)
    es_delicado = models.BooleanField(default=False)
    
    cliente = models.ForeignKey(
        ClienteLavanderia,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articulos"
    )

    def __str__(self):
        return f"{self.tipo_prenda} ({self.color})"


# ------------------------------------------------------
# Máquina
# ------------------------------------------------------
class MaquinaLavanderia(models.Model):
    tipo_maquina = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    capacidad_kg = models.DecimalField(max_digits=5, decimal_places=2)
    estado_operativo = models.CharField(max_length=50)
    ultima_revision = models.DateField()
    num_serie = models.CharField(max_length=50)
    es_lavadora = models.BooleanField(default=False)
    es_secadora = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo_maquina} {self.marca} {self.modelo}"


# ------------------------------------------------------
# Pedido
# ------------------------------------------------------
class PedidoLavanderia(models.Model):
    cliente = models.ForeignKey(
        ClienteLavanderia,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    fecha_recepcion = models.DateTimeField()
    fecha_entrega_estimada = models.DateField()
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)
    estado_pedido = models.CharField(max_length=50)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    
    empleado_recepcion = models.ForeignKey(
        EmpleadoLavanderia,
        on_delete=models.SET_NULL,
        null=True,
        related_name="pedidos_recibidos"
    )
    
    comentarios_cliente = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.cliente}"


# ------------------------------------------------------
# Detalle del Pedido
# ------------------------------------------------------
class DetallePedidoLavanderia(models.Model):
    pedido = models.ForeignKey(
        PedidoLavanderia,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    articulo = models.ForeignKey(
        ArticuloRopa,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    cantidad = models.IntegerField()
    tipo_servicio = models.CharField(max_length=50)
    costo_servicio_individual = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal_item = models.DecimalField(max_digits=10, decimal_places=2)
    manchas_detectadas = models.TextField(null=True, blank=True)
    instrucciones_item = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Detalle {self.id} del Pedido {self.pedido.id}"


# ------------------------------------------------------
# Reporte Operacional
# ------------------------------------------------------
class ReporteOperacional(models.Model):
    fecha_reporte = models.DateField()
    empleado = models.ForeignKey(
        EmpleadoLavanderia,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reportes"
    )
    num_pedidos_procesados = models.IntegerField()
    kg_ropa_procesada = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_inactividad_maquinas = models.IntegerField()
    observaciones_turno = models.TextField(null=True, blank=True)
    consumo_agua_litros = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reporte {self.id} - {self.fecha_reporte}"
