with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

# ── 1. Admin entrenamiento_crear ──────────────────────────────────────────────
old1 = (
    "            Entrenamiento.objects.create(\r\n"
    "                titulo=titulo, equipo_id=equipo_id, entrenador_id=entrenador_id,\r\n"
    "                fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,\r\n"
    "                lugar=lugar, descripcion=descripcion\r\n"
    "            )\r\n"
    "            messages.success(request, f'Entrenamiento \"{titulo}\" creado correctamente.')\r\n"
    "\r\n"
    "    return render(request, 'panel/entrenamientos/form.html', {"
)
new1 = (
    "            ent = Entrenamiento.objects.create(\r\n"
    "                titulo=titulo, equipo_id=equipo_id, entrenador_id=entrenador_id,\r\n"
    "                fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,\r\n"
    "                lugar=lugar, descripcion=descripcion\r\n"
    "            )\r\n"
    "            _notificar_entrenamiento(ent, es_nuevo=True, emisor=request.user)\r\n"
    "            messages.success(request, f'Entrenamiento \"{titulo}\" creado correctamente.')\r\n"
    "\r\n"
    "    return render(request, 'panel/entrenamientos/form.html', {"
)
assert old1 in content, "NO ENCONTRADO: bloque 1"
content = content.replace(old1, new1, 1)
print("OK 1")

# ── 2. Admin entrenamiento_editar ─────────────────────────────────────────────
old2 = (
    "        entrenamiento.save()\r\n"
    "        messages.success(request, f'Entrenamiento \"{entrenamiento.titulo}\" actualizado.')\r\n"
    "    return render(request, 'panel/entrenamientos/form.html', {"
)
new2 = (
    "        entrenamiento.save()\r\n"
    "        _notificar_entrenamiento(entrenamiento, es_nuevo=False, emisor=request.user)\r\n"
    "        messages.success(request, f'Entrenamiento \"{entrenamiento.titulo}\" actualizado.')\r\n"
    "    return render(request, 'panel/entrenamientos/form.html', {"
)
assert old2 in content, "NO ENCONTRADO: bloque 2"
content = content.replace(old2, new2, 1)
print("OK 2")

# ── 3. Entrenador ent_entrenamiento_crear — renombrar variable ─────────────────
old3 = (
    "            Entrenamiento.objects.create(\r\n"
    "                titulo=titulo, equipo_id=equipo_id,\r\n"
    "                entrenador=request.user,\r\n"
)
new3 = (
    "            ent = Entrenamiento.objects.create(\r\n"
    "                titulo=titulo, equipo_id=equipo_id,\r\n"
    "                entrenador=request.user,\r\n"
)
assert old3 in content, "NO ENCONTRADO: bloque 3"
content = content.replace(old3, new3, 1)
print("OK 3")

# 3b — agregar notificacion despues del cierre del create del entrenador
old3b = (
    "            )\r\n"
    "            messages.success(request, f'Entrenamiento \"{titulo}\" creado correctamente.')\r\n"
    "            return ent_entrenamientos_lista(request)"
)
new3b = (
    "            )\r\n"
    "            _notificar_entrenamiento(ent, es_nuevo=True, emisor=request.user)\r\n"
    "            messages.success(request, f'Entrenamiento \"{titulo}\" creado correctamente.')\r\n"
    "            return ent_entrenamientos_lista(request)"
)
assert old3b in content, "NO ENCONTRADO: bloque 3b"
content = content.replace(old3b, new3b, 1)
print("OK 3b")

# ── 4. Entrenador ent_entrenamiento_editar ────────────────────────────────────
old4 = (
    "        entrenamiento.save()\r\n"
    "        messages.success(request, f'Entrenamiento \"{entrenamiento.titulo}\" actualizado.')\r\n"
    "\r\n"
    "    return render(request, 'entrenador/entrenamientos/form.html', {"
)
new4 = (
    "        entrenamiento.save()\r\n"
    "        _notificar_entrenamiento(entrenamiento, es_nuevo=False, emisor=request.user)\r\n"
    "        messages.success(request, f'Entrenamiento \"{entrenamiento.titulo}\" actualizado.')\r\n"
    "\r\n"
    "    return render(request, 'entrenador/entrenamientos/form.html', {"
)
assert old4 in content, "NO ENCONTRADO: bloque 4"
content = content.replace(old4, new4, 1)
print("OK 4")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
