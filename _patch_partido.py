with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

# ── 1. Admin admin_partido_crear ──────────────────────────────────────────────
old1 = (
    "            PartidoCalendario.objects.create(\r\n"
    "                equipo_propio_id=equipo_id,\r\n"
    "                equipo_rival=equipo_rival,\r\n"
    "                fecha=fecha, hora=hora,\r\n"
    "                cancha=cancha, descripcion=descripcion,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            messages.success(request, 'Partido creado correctamente.')\r\n"
    "            return admin_partidos(request)"
)
new1 = (
    "            partido = PartidoCalendario.objects.create(\r\n"
    "                equipo_propio_id=equipo_id,\r\n"
    "                equipo_rival=equipo_rival,\r\n"
    "                fecha=fecha, hora=hora,\r\n"
    "                cancha=cancha, descripcion=descripcion,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_partido(partido, es_nuevo=True, emisor=request.user)\r\n"
    "            messages.success(request, 'Partido creado correctamente.')\r\n"
    "            return admin_partidos(request)"
)
assert old1 in content, "NO ENCONTRADO: bloque 1"
content = content.replace(old1, new1, 1)
print("OK 1")

# ── 2. Admin admin_partido_editar ─────────────────────────────────────────────
old2 = (
    "        partido.save()\r\n"
    "        messages.success(request, 'Partido actualizado correctamente.')\r\n"
    "        return admin_partidos(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/partidos/form.html', {"
)
new2 = (
    "        partido.save()\r\n"
    "        _notificar_partido(partido, es_nuevo=False, emisor=request.user)\r\n"
    "        messages.success(request, 'Partido actualizado correctamente.')\r\n"
    "        return admin_partidos(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/partidos/form.html', {"
)
assert old2 in content, "NO ENCONTRADO: bloque 2"
content = content.replace(old2, new2, 1)
print("OK 2")

# ── 3. Entrenador ent_partido_crear ───────────────────────────────────────────
old3 = (
    "            PartidoCalendario.objects.create(\r\n"
    "                equipo_propio_id=equipo_id,\r\n"
    "                equipo_rival=equipo_rival,\r\n"
    "                fecha=fecha, hora=hora,\r\n"
    "                cancha=cancha, descripcion=descripcion,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            messages.success(request, 'Partido creado correctamente.')\r\n"
    "            return ent_partidos(request)"
)
new3 = (
    "            partido = PartidoCalendario.objects.create(\r\n"
    "                equipo_propio_id=equipo_id,\r\n"
    "                equipo_rival=equipo_rival,\r\n"
    "                fecha=fecha, hora=hora,\r\n"
    "                cancha=cancha, descripcion=descripcion,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_partido(partido, es_nuevo=True, emisor=request.user)\r\n"
    "            messages.success(request, 'Partido creado correctamente.')\r\n"
    "            return ent_partidos(request)"
)
assert old3 in content, "NO ENCONTRADO: bloque 3"
content = content.replace(old3, new3, 1)
print("OK 3")

# ── 4. Entrenador ent_partido_editar ──────────────────────────────────────────
old4 = (
    "            partido.save()\r\n"
    "            messages.success(request, 'Partido actualizado correctamente.')\r\n"
    "            return ent_partidos(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/partidos/form.html', {"
)
new4 = (
    "            partido.save()\r\n"
    "            _notificar_partido(partido, es_nuevo=False, emisor=request.user)\r\n"
    "            messages.success(request, 'Partido actualizado correctamente.')\r\n"
    "            return ent_partidos(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/partidos/form.html', {"
)
assert old4 in content, "NO ENCONTRADO: bloque 4"
content = content.replace(old4, new4, 1)
print("OK 4")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
