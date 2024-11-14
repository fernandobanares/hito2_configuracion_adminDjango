from django.db import models
from django.contrib.auth.models import User

class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('oficina', 'Oficina'),
        ('local_comercial', 'Local Comercial'),
        ('terreno', 'Terreno'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    m2_construidos = models.DecimalField(max_digits=5, decimal_places=2)
    m2_totales = models.DecimalField(max_digits=5, decimal_places=2)
    estacionamientos = models.IntegerField(default=0)
    habitaciones = models.IntegerField(default=1)
    banos = models.IntegerField(default=1)
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=100)
    tipo_inmueble = models.CharField(max_length=50, choices=TIPO_INMUEBLE_CHOICES, default='casa')
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    arrendador = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'tipo_usuario': 'arrendador'})

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='arrendatario')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.tipo_usuario}"

class SolicitudArriendo(models.Model):
    ESTADO_SOLICITUD_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    inmueble = models.ForeignKey('Inmueble', on_delete=models.CASCADE, related_name='solicitudes')
    arrendatario = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'arrendatario'})
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.arrendatario} para {self.inmueble} - {self.estado}"

