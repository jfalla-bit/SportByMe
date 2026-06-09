with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

# Agregar notificacion de convocatoria despues de convocatoria.save()
old = (
    "        convocatoria.save()\r\n"
    "        messages.success(request, f'Convocatoria guardada: {len(ids_seleccionados)} jugador(es) convocado(s).')\r\n"
    "        return ent_partidos(request)"
)
new = (
    "        convocatoria.save()\r\n"
    "        # Notificar a cada jugador convocado\r\n"
    "        jugadores_convocados = Jugador.objects.filter(\r\n"
    "            id__in=ids_seleccionados\r\n"
    "        ).select_related('usuario')\r\n"
    "        asunto_conv = f'Convocatoria: {partido.equipo_propio.nombre} vs {partido.equipo_rival}'\r\n"
    "        mensaje_conv = (\r\n"
    "            f'Has sido convocado para el siguiente partido:\\n\\n'\r\n"
    "            f'Equipo:  {partido.equipo_propio.nombre}\\n'\r\n"
    "            f'Rival:   {partido.equipo_rival}\\n'\r\n"
    "            f'Fecha:   {partido.fecha.strftime(\"%d/%m/%Y\")}\\n'\r\n"
    "            f'Hora:    {partido.hora.strftime(\"%H:%M\")}\\n'\r\n"
    "            f'Lugar:   {partido.cancha or \"Por confirmar\"}'\r\n"
    "            + (f'\\nNota:    {convocatoria.nota}' if convocatoria.nota else '')\r\n"
    "        )\r\n"
    "        Notificacion.objects.bulk_create([\r\n"
    "            Notificacion(usuario=j.usuario, asunto=asunto_conv, mensaje=mensaje_conv, emisor=request.user)\r\n"
    "            for j in jugadores_convocados\r\n"
    "        ])\r\n"
    "        for j in jugadores_convocados:\r\n"
    "            if j.usuario.email and '@' in j.usuario.email:\r\n"
    "                try:\r\n"
    "                    send_mail(\r\n"
    "                        subject=asunto_conv,\r\n"
    "                        message=mensaje_conv,\r\n"
    "                        from_email=django_settings.DEFAULT_FROM_EMAIL,\r\n"
    "                        recipient_list=[j.usuario.email],\r\n"
    "                        fail_silently=True,\r\n"
    "                    )\r\n"
    "                except Exception:\r\n"
    "                    pass\r\n"
    "        messages.success(request, f'Convocatoria guardada: {len(ids_seleccionados)} jugador(es) convocado(s).')\r\n"
    "        return ent_partidos(request)"
)

assert old in content, "NO ENCONTRADO: bloque convocatoria"
content = content.replace(old, new, 1)
print("OK convocatoria")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
