from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('entrenador', 'Entrenador'),
        ('deportista', 'Deportista'),
        ('acudiente', 'Acudiente'),
        ('pendiente', 'Pendiente'),
    ]
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='deportista')
    documento  = models.CharField(max_length=20, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def is_administrador(self):
        return self.role == 'administrador'

    def is_entrenador(self):
        return self.role == 'entrenador'

    def is_deportista(self):
        return self.role == 'deportista'

    def is_acudiente(self):
        return self.role == 'acudiente'


class Categoria(models.Model):
    SUBCATEGORIA_CHOICES = [
        ('sub10', 'Sub-10 (8 a 10 años)'),
        ('sub12', 'Sub-12 (11 y 12 años)'),
        ('sub14', 'Sub-14 (13 y 14 años)'),
        ('sub16', 'Sub-16 (15 y 16 años)'),
        ('sub18', 'Sub-18 (17 años)'),
        ('sub20', 'Sub-20 (18 a 20 años)'),
    ]
    EDAD_RANGOS = {
        'sub10': (8, 10),
        'sub12': (11, 12),
        'sub14': (13, 14),
        'sub16': (15, 16),
        'sub18': (17, 17),
        'sub20': (18, 20),
    }
    nombre       = models.CharField(max_length=100)
    descripcion  = models.TextField(blank=True)
    subcategoria = models.CharField(max_length=10, choices=SUBCATEGORIA_CHOICES, blank=True)
    edad_minima  = models.PositiveIntegerField(null=True, blank=True)
    edad_maxima  = models.PositiveIntegerField(null=True, blank=True)
    activo       = models.BooleanField(default=True)
    creado       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='equipos')
    entrenador = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True,
                                   limit_choices_to={'role': 'entrenador'}, related_name='equipos')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'equipos'

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    usuario = models.OneToOneField(UserModel, on_delete=models.CASCADE,
                                   limit_choices_to={'role': 'deportista'}, related_name='jugador')
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True, related_name='jugadores')
    posicion = models.CharField(max_length=50, blank=True)
    numero_camiseta = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'jugadores'

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.equipo}"


class Entrenamiento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='entrenamientos')
    entrenador = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                   limit_choices_to={'role': 'entrenador'}, related_name='entrenamientos')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=200, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'entrenamientos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"


class Torneo(models.Model):
    ESTADO_CHOICES = [
        ('planificado', 'Planificado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='torneos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    lugar = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificado')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'torneos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.nombre


class Partido(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidos')
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    fecha = models.DateTimeField()
    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)
    lugar = models.CharField(max_length=200, blank=True)
    jugado = models.BooleanField(default=False)

    class Meta:
        db_table = 'partidos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"


class Finanza(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    CATEGORIA_CHOICES = [
        ('cuota', 'Cuota de Jugador'),
        ('patrocinio', 'Patrocinio'),
        ('equipamiento', 'Equipamiento'),
        ('instalaciones', 'Instalaciones'),
        ('transporte', 'Transporte'),
        ('otro', 'Otro'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='otro')
    descripcion = models.CharField(max_length=300)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    registrado_por = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    pago = models.OneToOneField('Pago', on_delete=models.SET_NULL, null=True, blank=True, related_name='finanza')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - {self.monto}"


class Evaluacion(models.Model):
    """Evaluaciones realizadas a un deportista por su entrenador"""
    TIPO_CHOICES = [
        ('tecnica',  'Técnica'),
        ('tactica',  'Táctica'),
        ('fisica',   'Física'),
    ]
    jugador     = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='evaluaciones')
    entrenador  = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                    limit_choices_to={'role': 'entrenador'}, related_name='evaluaciones')
    titulo      = models.CharField(max_length=200)
    tipo        = models.CharField(max_length=10, choices=TIPO_CHOICES, default='tecnica')
    descripcion = models.TextField(blank=True)
    puntaje     = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True,
                                      help_text='Puntaje de 0 a 5')
    observaciones = models.TextField(blank=True)
    fecha       = models.DateField()
    creado      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'evaluaciones'
        ordering  = ['-fecha']

    def __str__(self):
        return f"{self.titulo} - {self.jugador}"


class ConceptoPago(models.Model):
    """Conceptos de pago configurables por el administrador."""
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    monto_base  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo      = models.BooleanField(default=True)
    creado      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conceptos_pago'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    """Pagos asociados a un deportista (cuotas, inscripciones, etc.)"""
    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('pagado',      'Pagado'),
        ('vencido',     'Vencido'),
    ]
    CONCEPTO_CHOICES = [
        ('cuota_mensual',  'Cuota Mensual'),
        ('inscripcion',    'Inscripción'),
        ('equipamiento',   'Equipamiento'),
        ('torneo',         'Torneo'),
        ('otro',           'Otro'),
    ]
    METODO_CHOICES = [
        ('efectivo',      'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta',       'Tarjeta'),
        ('otro',          'Otro'),
    ]
    jugador       = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='pagos')
    concepto      = models.CharField(max_length=20, choices=CONCEPTO_CHOICES, default='cuota_mensual')
    descripcion   = models.CharField(max_length=300)
    monto         = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago    = models.DateField(null=True, blank=True)
    estado        = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago   = models.CharField(max_length=20, choices=METODO_CHOICES, blank=True, default='')
    registrado_por = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                       related_name='pagos_registrados')
    creado        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_vencimiento']

    def __str__(self):
        return f"{self.jugador} - {self.concepto} - {self.estado}"

    @classmethod
    def marcar_vencidos(cls):
        """Marca como VENCIDO todo pago pendiente cuya fecha_vencimiento ya pasó.
        No afecta pagos en_revision ni pagados."""
        from django.utils import timezone
        hoy = timezone.now().date()
        return cls.objects.filter(
            estado='pendiente',
            fecha_vencimiento__lt=hoy
        ).update(estado='vencido')


class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('asistio',     'Asistió'),
        ('no_asistio',  'No Asistió'),
        ('justificado', 'Justificado'),
    ]
    entrenamiento  = models.ForeignKey('Entrenamiento', on_delete=models.CASCADE, related_name='asistencias')
    jugador        = models.ForeignKey('Jugador', on_delete=models.CASCADE, related_name='asistencias')
    estado         = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='asistio')
    observacion    = models.CharField(max_length=200, blank=True)
    registrado_por = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='asistencias_registradas')
    creado         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'asistencias'
        unique_together = ('entrenamiento', 'jugador')
        ordering        = ['jugador__usuario__last_name']

    def __str__(self):
        return f"{self.entrenamiento} — {self.jugador} — {self.estado}"


class Convocatoria(models.Model):
    """Convocatoria de jugadores para un partido del calendario."""
    partido  = models.OneToOneField('PartidoCalendario', on_delete=models.CASCADE, related_name='convocatoria')
    jugadores = models.ManyToManyField('Jugador', related_name='convocatorias', blank=True)
    nota     = models.TextField(blank=True)
    creado   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'convocatorias'

    def __str__(self):
        return f"Convocatoria {self.partido}"


class RespuestaConvocatoria(models.Model):
    """Respuesta del deportista a una convocatoria (confirma o rechaza)."""
    RESPUESTA_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('rechazado',  'Rechazado'),
    ]
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='respuestas')
    jugador      = models.ForeignKey('Jugador', on_delete=models.CASCADE, related_name='respuestas_convocatoria')
    respuesta    = models.CharField(max_length=15, choices=RESPUESTA_CHOICES)
    creado       = models.DateTimeField(auto_now_add=True)
    actualizado  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = 'respuestas_convocatoria'
        unique_together = ('convocatoria', 'jugador')

    def __str__(self):
        return f"{self.jugador} — {self.convocatoria} — {self.respuesta}"


class EstadisticaPartido(models.Model):
    """Estadísticas individuales de un jugador en un partido."""
    partido       = models.ForeignKey('PartidoCalendario', on_delete=models.CASCADE, related_name='estadisticas')
    jugador       = models.ForeignKey('Jugador', on_delete=models.CASCADE, related_name='estadisticas_partido')
    goles         = models.PositiveIntegerField(default=0)
    asistencias   = models.PositiveIntegerField(default=0)
    tarjeta_amarilla = models.BooleanField(default=False)
    tarjeta_roja     = models.BooleanField(default=False)
    calificacion  = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True,
                                        help_text='Calificacion de 1 a 10')
    registrado_por = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='estadisticas_registradas')
    creado        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'estadisticas_partido'
        unique_together = ('partido', 'jugador')
        ordering        = ['jugador__usuario__last_name']

    def __str__(self):
        return f"{self.jugador} — {self.partido}"


class PartidoCalendario(models.Model):
    """Partido programado por admin o entrenador, independiente de un torneo."""
    equipo_propio    = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_propios')
    equipo_rival     = models.CharField(max_length=200)
    fecha            = models.DateField()
    hora             = models.TimeField()
    cancha           = models.CharField(max_length=200, blank=True)
    descripcion      = models.TextField(blank=True)
    goles_favor      = models.PositiveIntegerField(null=True, blank=True)
    goles_contra     = models.PositiveIntegerField(null=True, blank=True)
    observaciones    = models.TextField(blank=True)
    registrado_por   = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='partidos_registrados')
    creado           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partidos_calendario'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"{self.equipo_propio} vs {self.equipo_rival} — {self.fecha}"


class ObservacionDeportista(models.Model):
    """Observaciones técnicas, tácticas o físicas de un deportista registradas por el entrenador."""
    TIPO_CHOICES = [
        ('tecnica',  'Técnica'),
        ('tactica',  'Táctica'),
        ('fisica',   'Física'),
    ]
    jugador        = models.ForeignKey('Jugador', on_delete=models.CASCADE, related_name='observaciones')
    entrenador     = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                       limit_choices_to={'role': 'entrenador'}, related_name='observaciones_registradas')
    tipo           = models.CharField(max_length=10, choices=TIPO_CHOICES, default='tecnica')
    fecha          = models.DateField()
    descripcion    = models.TextField()
    creado         = models.DateTimeField(auto_now_add=True)
    actualizado    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'observaciones_deportista'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.jugador} — {self.fecha}"


class Acudiente(models.Model):
    """Vincula un usuario con rol acudiente al deportista a su cargo."""
    usuario  = models.OneToOneField(UserModel, on_delete=models.CASCADE,
                                    limit_choices_to={'role': 'acudiente'}, related_name='acudiente')
    jugador  = models.ForeignKey('Jugador', on_delete=models.CASCADE, related_name='acudientes')
    parentesco = models.CharField(max_length=50, blank=True)
    creado   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'acudientes'

    def __str__(self):
        return f"{self.usuario.get_full_name()} → {self.jugador}"


class PagoEntrenador(models.Model):
    """Nómina mensual pagada a un entrenador por el administrador."""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado',    'Pagado'),
    ]
    METODO_CHOICES = [
        ('efectivo',      'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta',       'Tarjeta'),
        ('otro',          'Otro'),
    ]
    entrenador     = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                                       limit_choices_to={'role': 'entrenador'},
                                       related_name='pagos_nomina')
    mes            = models.PositiveIntegerField(help_text='Mes (1-12)')
    anio           = models.PositiveIntegerField(help_text='Año')
    monto          = models.DecimalField(max_digits=10, decimal_places=2)
    estado         = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago    = models.CharField(max_length=20, choices=METODO_CHOICES, blank=True, default='')
    descripcion    = models.CharField(max_length=300, blank=True)
    fecha_pago     = models.DateField(null=True, blank=True)
    registrado_por = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,
                                       related_name='nominas_registradas')
    creado         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'pagos_entrenador'
        ordering        = ['-anio', '-mes']
        unique_together = ('entrenador', 'mes', 'anio')

    def __str__(self):
        return f"{self.entrenador.get_full_name()} — {self.mes}/{self.anio} — {self.estado}"


class Notificacion(models.Model):
    """Notificaciones enviadas por el administrador a los usuarios."""
    usuario  = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notificaciones')
    emisor   = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificaciones_enviadas')
    asunto   = models.CharField(max_length=200)
    mensaje  = models.TextField()
    leida    = models.BooleanField(default=False)
    creado   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'
        ordering = ['-creado']

    def __str__(self):
        return f"{self.usuario.username} - {self.asunto}"
