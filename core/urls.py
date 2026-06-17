from django.urls import path
from . import views
from django.http import HttpResponse
urlpatterns = [
    path('', lambda request: HttpResponse("Sistema SportByMe activo")),
    # Dashboards por rol
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('entrenador-dashboard/', views.entrenador_dashboard, name='entrenador_dashboard'),
    path('deportista-dashboard/', views.deportista_dashboard, name='deportista_dashboard'),

    # Panel Admin: Usuarios
    path('panel/usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('panel/usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('panel/usuarios/<int:user_id>/', views.usuario_detalle, name='usuario_detalle'),
    path('panel/usuarios/<int:user_id>/editar/', views.usuario_editar, name='usuario_editar'),
    path('panel/usuarios/<int:user_id>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),

    # Panel Admin: Categorias
    path('panel/categorias/', views.categorias_lista, name='categorias_lista'),
    path('panel/categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('panel/categorias/<int:cat_id>/editar/', views.categoria_editar, name='categoria_editar'),
    path('panel/categorias/<int:cat_id>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),

    # Panel Admin: Equipos
    path('panel/equipos/', views.equipos_lista, name='equipos_lista'),
    path('panel/equipos/crear/', views.equipo_crear, name='equipo_crear'),
    path('panel/equipos/<int:equipo_id>/editar/', views.equipo_editar, name='equipo_editar'),
    path('panel/equipos/<int:equipo_id>/eliminar/', views.equipo_eliminar, name='equipo_eliminar'),
    path('panel/equipos/<int:equipo_id>/jugadores/', views.admin_equipo_jugadores, name='admin_equipo_jugadores'),

    # Panel Admin: Entrenamientos
    path('panel/entrenamientos/', views.entrenamientos_lista, name='entrenamientos_lista'),
    path('panel/entrenamientos/crear/', views.entrenamiento_crear, name='entrenamiento_crear'),
    path('panel/entrenamientos/<int:ent_id>/editar/', views.entrenamiento_editar, name='entrenamiento_editar'),
    path('panel/entrenamientos/<int:ent_id>/eliminar/', views.entrenamiento_eliminar, name='entrenamiento_eliminar'),

    # Panel Admin: Torneos
    path('panel/torneos/', views.torneos_lista, name='torneos_lista'),
    path('panel/torneos/crear/', views.torneo_crear, name='torneo_crear'),
    path('panel/torneos/<int:torneo_id>/editar/', views.torneo_editar, name='torneo_editar'),
    path('panel/torneos/<int:torneo_id>/eliminar/', views.torneo_eliminar, name='torneo_eliminar'),

    # Panel Admin: Finanzas
    path('panel/finanzas/', views.finanzas_lista, name='finanzas_lista'),
    path('panel/finanzas/crear/', views.finanza_crear, name='finanza_crear'),
    path('panel/finanzas/<int:fin_id>/eliminar/', views.finanza_eliminar, name='finanza_eliminar'),

    # Panel Admin: Pagos
    path('panel/pagos/', views.admin_pagos_lista, name='admin_pagos_lista'),
    path('panel/pagos/crear/', views.admin_pago_crear, name='admin_pago_crear'),
    path('panel/pagos/<int:pago_id>/editar/', views.admin_pago_editar, name='admin_pago_editar'),
    path('panel/pagos/<int:pago_id>/eliminar/', views.admin_pago_eliminar, name='admin_pago_eliminar'),
    path('panel/pagos/<int:pago_id>/marcar-pagado/', views.admin_pago_marcar_pagado, name='admin_pago_marcar_pagado'),
    path('panel/pagos/<int:pago_id>/marcar-pendiente/', views.admin_pago_marcar_pendiente, name='admin_pago_marcar_pendiente'),
    path('panel/pagos/<int:pago_id>/factura/', views.admin_factura_pago, name='admin_factura_pago'),
    path('panel/facturas/', views.admin_facturas_lista, name='admin_facturas_lista'),
    path('panel/jugadores/<int:jug_id>/cuenta/', views.admin_cuenta_deportista, name='admin_cuenta_deportista'),

    # Panel Admin: Conceptos de Pago
    path('panel/conceptos/', views.admin_conceptos_lista, name='admin_conceptos_lista'),
    path('panel/conceptos/crear/', views.admin_concepto_crear, name='admin_concepto_crear'),
    path('panel/conceptos/<int:concepto_id>/editar/', views.admin_concepto_editar, name='admin_concepto_editar'),
    path('panel/conceptos/<int:concepto_id>/eliminar/', views.admin_concepto_eliminar, name='admin_concepto_eliminar'),

    # Panel Admin: Asistencia
    path('panel/asistencia/', views.admin_asistencia, name='admin_asistencia'),
    path('panel/asistencia/deportista/', views.admin_asistencia_deportista, name='admin_asistencia_deportista'),

    # Panel Admin: Partidos
    path('panel/partidos/', views.admin_partidos, name='admin_partidos'),
    path('panel/partidos/crear/', views.admin_partido_crear, name='admin_partido_crear'),
    path('panel/partidos/<int:partido_id>/editar/', views.admin_partido_editar, name='admin_partido_editar'),
    path('panel/partidos/<int:partido_id>/eliminar/', views.admin_partido_eliminar, name='admin_partido_eliminar'),

    # Panel Admin: Estadisticas de partidos
    path('panel/estadisticas/', views.admin_estadisticas_equipo, name='admin_estadisticas_equipo'),
    path('panel/estadisticas/jugador/', views.admin_estadisticas_jugador, name='admin_estadisticas_jugador'),
    path('panel/reporte/rendimiento/<str:tipo>/<int:objeto_id>/pdf/', views.admin_reporte_rendimiento_pdf, name='admin_reporte_rendimiento_pdf'),
    path('panel/reportes/rendimiento/', views.admin_reporte_rendimiento, name='admin_reporte_rendimiento'),

    # Panel Admin: Reportes
    path('panel/reportes/deportistas/', views.admin_reporte_deportistas, name='admin_reporte_deportistas'),
    path('panel/reportes/asistencia/', views.admin_reporte_asistencia, name='admin_reporte_asistencia'),
    path('panel/reportes/entrenamientos/', views.admin_reporte_entrenamientos, name='admin_reporte_entrenamientos'),
    path('panel/reportes/partidos/', views.admin_reporte_partidos, name='admin_reporte_partidos'),
    path('panel/reportes/financiero/', views.admin_reporte_financiero, name='admin_reporte_financiero'),
    path('panel/reportes/pagos/', views.admin_reporte_pagos, name='admin_reporte_pagos'),

    # Panel Entrenador: Reportes
    path('entrenador/reportes/asistencia/', views.ent_reporte_asistencia, name='ent_reporte_asistencia'),
    path('entrenador/reportes/entrenamientos/', views.ent_reporte_entrenamientos, name='ent_reporte_entrenamientos'),
    path('entrenador/reportes/partidos/', views.ent_reporte_partidos, name='ent_reporte_partidos'),
    path('entrenador/reportes/rendimiento/', views.ent_reporte_rendimiento, name='ent_reporte_rendimiento'),
    path('panel/pdf/<str:modulo>/', views.exportar_pdf, name='exportar_pdf'),
    path('panel/csv/<str:modulo>/', views.exportar_csv, name='exportar_csv'),
    path('panel/reportes/estadisticas-rendimiento/', views.admin_estadisticas_rendimiento, name='admin_estadisticas_rendimiento'),
    path('panel/reportes/estadisticas-asistencia/', views.admin_estadisticas_asistencia, name='admin_estadisticas_asistencia'),
    path('panel/reportes/estadisticas-partidos/', views.admin_estadisticas_partidos, name='admin_estadisticas_partidos'),
    path('entrenador/reportes/estadisticas-rendimiento/', views.ent_estadisticas_rendimiento, name='ent_estadisticas_rendimiento'),
    path('entrenador/reportes/estadisticas-asistencia/', views.ent_estadisticas_asistencia, name='ent_estadisticas_asistencia'),
    path('entrenador/reportes/estadisticas-partidos/', views.ent_estadisticas_partidos, name='ent_estadisticas_partidos'),
    path('panel/correos/', views.admin_enviar_correo, name='admin_enviar_correo'),
    path('panel/correos/usuario/', views.admin_enviar_correo_usuario, name='admin_enviar_correo_usuario'),
    path('panel/correos/enviados/', views.admin_mensajes_enviados, name='admin_mensajes_enviados'),
    path('panel/correos/enviados/<int:noti_id>/eliminar/', views.admin_mensaje_eliminar, name='admin_mensaje_eliminar'),
    path('panel/notificaciones/', views.admin_notificaciones, name='admin_notificaciones'),
    path('panel/notificaciones/leer-todos/', views.admin_notificaciones_leer_todos, name='admin_notificaciones_leer_todos'),
    path('panel/notificaciones/<int:noti_id>/eliminar/', views.admin_notificacion_eliminar, name='admin_notificacion_eliminar'),
    path('entrenador/mensajes/enviar/', views.ent_enviar_mensaje, name='ent_enviar_mensaje'),
    path('entrenador/mensajes/grupo/', views.ent_enviar_mensaje_grupo, name='ent_enviar_mensaje_grupo'),
    path('entrenador/mensajes/enviados/', views.ent_mensajes_enviados, name='ent_mensajes_enviados'),
    path('entrenador/mensajes/enviados/<int:noti_id>/eliminar/', views.ent_mensaje_eliminar, name='ent_mensaje_eliminar'),
    path('notificacion/<int:noti_id>/leer/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),

    # Mensajes entrenador
    path('entrenador/mensajes/', views.ent_mensajes, name='ent_mensajes'),
    path('entrenador/mensajes/leer-todos/', views.ent_mensajes_leer_todos, name='ent_mensajes_leer_todos'),
    path('entrenador/mensajes/<int:noti_id>/eliminar/', views.ent_notificacion_eliminar, name='ent_notificacion_eliminar'),

    # Mensajes deportista
    path('deportista/mensajes/', views.dep_mensajes, name='dep_mensajes'),
    path('deportista/mensajes/leer-todos/', views.dep_mensajes_leer_todos, name='dep_mensajes_leer_todos'),
    path('deportista/mensajes/<int:noti_id>/eliminar/', views.dep_notificacion_eliminar, name='dep_notificacion_eliminar'),

    # Panel Entrenador: Entrenamientos
    path('entrenador/mis-entrenamientos/', views.ent_entrenamientos_lista, name='ent_entrenamientos_lista'),
    path('entrenador/mis-entrenamientos/crear/', views.ent_entrenamiento_crear, name='ent_entrenamiento_crear'),
    path('entrenador/mis-entrenamientos/<int:ent_id>/editar/', views.ent_entrenamiento_editar, name='ent_entrenamiento_editar'),
    path('entrenador/mis-entrenamientos/<int:ent_id>/eliminar/', views.ent_entrenamiento_eliminar, name='ent_entrenamiento_eliminar'),
    path('entrenador/mis-entrenamientos/<int:ent_id>/asistencia/', views.ent_asistencia, name='ent_asistencia'),

    # Panel Entrenador: Equipos
    path('entrenador/mis-equipos/', views.ent_equipos_lista, name='ent_equipos_lista'),
    path('entrenador/mis-equipos/<int:equipo_id>/', views.ent_equipo_detalle, name='ent_equipo_detalle'),

    # Panel Entrenador: Jugadores
    path('entrenador/jugadores/', views.ent_jugadores_lista, name='ent_jugadores_lista'),
    path('entrenador/jugadores/crear/', views.ent_jugador_crear, name='ent_jugador_crear'),
    path('entrenador/jugadores/<int:jug_id>/editar/', views.ent_jugador_editar, name='ent_jugador_editar'),
    path('entrenador/jugadores/<int:jug_id>/eliminar/', views.ent_jugador_eliminar, name='ent_jugador_eliminar'),

    # Panel Entrenador: Historial de jugador
    path('entrenador/jugadores/<int:jug_id>/historial/', views.ent_historial_jugador, name='ent_historial_jugador'),
    path('entrenador/reporte/<str:tipo>/<int:objeto_id>/pdf/', views.ent_reporte_rendimiento_pdf, name='ent_reporte_rendimiento_pdf'),

    # Panel Entrenador: Observaciones
    path('entrenador/observaciones/', views.ent_observaciones_lista, name='ent_observaciones_lista'),
    path('entrenador/observaciones/crear/', views.ent_observacion_crear, name='ent_observacion_crear'),
    path('entrenador/observaciones/<int:obs_id>/editar/', views.ent_observacion_editar, name='ent_observacion_editar'),
    path('entrenador/observaciones/<int:obs_id>/eliminar/', views.ent_observacion_eliminar, name='ent_observacion_eliminar'),

    # Panel Entrenador: Evaluaciones
    path('entrenador/evaluaciones/', views.ent_evaluaciones_lista, name='ent_evaluaciones_lista'),
    path('entrenador/evaluaciones/crear/', views.ent_evaluacion_crear, name='ent_evaluacion_crear'),
    path('entrenador/evaluaciones/<int:eval_id>/editar/', views.ent_evaluacion_editar, name='ent_evaluacion_editar'),
    path('entrenador/evaluaciones/<int:eval_id>/eliminar/', views.ent_evaluacion_eliminar, name='ent_evaluacion_eliminar'),

    # Panel Entrenador: Asistencia
    path('entrenador/asistencia/', views.ent_asistencia_consulta, name='ent_asistencia_consulta'),
    path('entrenador/asistencia/deportista/', views.ent_asistencia_deportista, name='ent_asistencia_deportista'),

    # Panel Entrenador: Partidos
    path('entrenador/partidos/', views.ent_partidos, name='ent_partidos'),
    path('entrenador/partidos/crear/', views.ent_partido_crear, name='ent_partido_crear'),
    path('entrenador/partidos/<int:partido_id>/editar/', views.ent_partido_editar, name='ent_partido_editar'),
    path('entrenador/partidos/<int:partido_id>/eliminar/', views.ent_partido_eliminar, name='ent_partido_eliminar'),
    path('entrenador/partidos/<int:partido_id>/convocatoria/', views.ent_convocatoria, name='ent_convocatoria'),
    path('entrenador/partidos/<int:partido_id>/resultado/', views.ent_resultado, name='ent_resultado'),
    path('entrenador/partidos/<int:partido_id>/estadisticas/', views.ent_estadisticas, name='ent_estadisticas'),

    # Panel Entrenador: Estadisticas de partidos
    path('entrenador/estadisticas/', views.ent_estadisticas_equipo, name='ent_estadisticas_equipo'),
    path('entrenador/estadisticas/jugador/', views.ent_estadisticas_jugador, name='ent_estadisticas_jugador'),

    # Panel Entrenador: Pagos
    path('entrenador/pagos/', views.ent_pagos_lista, name='ent_pagos_lista'),
    path('entrenador/pagos/crear/', views.ent_pago_crear, name='ent_pago_crear'),
    path('entrenador/pagos/<int:pago_id>/editar/', views.ent_pago_editar, name='ent_pago_editar'),
    path('entrenador/pagos/<int:pago_id>/eliminar/', views.ent_pago_eliminar, name='ent_pago_eliminar'),

    # Panel Entrenador: Nómina (solo lectura)
    path('entrenador/nomina/', views.ent_nomina_lista, name='ent_nomina_lista'),

    # Panel Admin: Nómina entrenadores
    path('panel/nomina/', views.admin_nomina_lista, name='admin_nomina_lista'),
    path('panel/nomina/crear/', views.admin_nomina_crear, name='admin_nomina_crear'),
    path('panel/nomina/<int:nomina_id>/editar/', views.admin_nomina_editar, name='admin_nomina_editar'),
    path('panel/nomina/<int:nomina_id>/eliminar/', views.admin_nomina_eliminar, name='admin_nomina_eliminar'),
    path('panel/nomina/<int:nomina_id>/marcar-pagado/', views.admin_nomina_marcar_pagado, name='admin_nomina_marcar_pagado'),

    # Carga masiva
    path('panel/carga-masiva/', views.carga_masiva, name='carga_masiva'),
    path('panel/carga-masiva/plantilla/<str:modulo>/', views.carga_plantilla, name='carga_plantilla'),
    path('panel/carga-masiva/usuarios/', views.carga_usuarios, name='carga_usuarios'),
    path('panel/carga-masiva/categorias/', views.carga_categorias, name='carga_categorias'),
    path('panel/carga-masiva/equipos/', views.carga_equipos, name='carga_equipos'),
    path('panel/carga-masiva/pagos/', views.carga_pagos, name='carga_pagos'),

    # Panel Deportista
    path('deportista/perfil/', views.dep_perfil, name='dep_perfil'),
    path('deportista/historial/', views.dep_historial, name='dep_historial'),
    path('deportista/entrenamientos/', views.dep_entrenamientos, name='dep_entrenamientos'),
    path('deportista/evaluaciones/', views.dep_evaluaciones, name='dep_evaluaciones'),
    path('deportista/pagos/', views.dep_pagos, name='dep_pagos'),
    path('deportista/pagos/<int:pago_id>/factura/', views.dep_factura_pago, name='dep_factura_pago'),
    path('deportista/pagos/<int:pago_id>/reportar/', views.dep_pago_reportar, name='dep_pago_reportar'),
    path('deportista/torneos/', views.dep_torneos, name='dep_torneos'),
    path('deportista/calendario/', views.dep_calendario, name='dep_calendario'),
    path('deportista/convocatorias/', views.dep_convocatorias, name='dep_convocatorias'),
    path('deportista/convocatorias/<int:conv_id>/responder/', views.dep_responder_convocatoria, name='dep_responder_convocatoria'),
    path('deportista/asistencia/', views.dep_asistencia_historial, name='dep_asistencia_historial'),
    path('deportista/rendimiento/', views.dep_rendimiento, name='dep_rendimiento'),
    path('deportista/partidos-resultados/', views.dep_partidos_resultados, name='dep_partidos_resultados'),
    path('deportista/estadisticas/', views.dep_estadisticas, name='dep_estadisticas'),

    # Panel Acudiente
    path('acudiente-dashboard/', views.acudiente_dashboard, name='acudiente_dashboard'),
    path('acudiente/deportista/', views.acu_deportista, name='acu_deportista'),
    path('acudiente/calendario/', views.acu_calendario, name='acu_calendario'),
    path('acudiente/convocatorias/', views.acu_convocatorias, name='acu_convocatorias'),
    path('acudiente/convocatorias/<int:conv_id>/responder/', views.acu_responder_convocatoria, name='acu_responder_convocatoria'),
    path('acudiente/asistencia/', views.acu_asistencia, name='acu_asistencia'),
    path('acudiente/rendimiento/', views.acu_rendimiento, name='acu_rendimiento'),
    path('acudiente/partidos-resultados/', views.acu_partidos_resultados, name='acu_partidos_resultados'),
    path('acudiente/pagos/', views.acu_pagos, name='acu_pagos'),
    path('acudiente/mensajes/', views.acu_mensajes, name='acu_mensajes'),
    path('acudiente/mensajes/leer-todos/', views.acu_mensajes_leer_todos, name='acu_mensajes_leer_todos'),
    path('acudiente/mensajes/<int:noti_id>/eliminar/', views.acu_notificacion_eliminar, name='acu_notificacion_eliminar'),
]
