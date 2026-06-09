with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

# ── Funcion auxiliar _notificar_pago ─────────────────────────────────────────
old0 = "def solo_admin(view_func):"
new0 = (
    "def _notificar_pago(pago, accion, emisor):\r\n"
    "    \"\"\"\r\n"
    "    Envia notificacion al deportista sobre un pago.\r\n"
    "    accion: 'registrado', 'actualizado', 'pagado', 'pendiente'\r\n"
    "    \"\"\"\r\n"
    "    etiquetas = {\r\n"
    "        'registrado': 'Nuevo pago registrado',\r\n"
    "        'actualizado': 'Pago actualizado',\r\n"
    "        'pagado':      'Pago confirmado',\r\n"
    "        'pendiente':   'Pago revertido a pendiente',\r\n"
    "    }\r\n"
    "    asunto  = f'{etiquetas.get(accion, \"Notificacion de pago\")}: {pago.descripcion}'\r\n"
    "    estado_display = dict(pago.ESTADO_CHOICES).get(pago.estado, pago.estado)\r\n"
    "    mensaje = (\r\n"
    "        f'Informacion sobre tu pago:\\n\\n'\r\n"
    "        f'Concepto:     {pago.get_concepto_display()}\\n'\r\n"
    "        f'Descripcion:  {pago.descripcion}\\n'\r\n"
    "        f'Monto:        {pago.monto}\\n'\r\n"
    "        f'Vencimiento:  {pago.fecha_vencimiento.strftime(\"%d/%m/%Y\")}\\n'\r\n"
    "        f'Estado:       {estado_display}'\r\n"
    "        + (f'\\nFecha pago:   {pago.fecha_pago.strftime(\"%d/%m/%Y\")}' if pago.fecha_pago else '')\r\n"
    "    )\r\n"
    "    usuario = pago.jugador.usuario\r\n"
    "    Notificacion.objects.create(usuario=usuario, asunto=asunto, mensaje=mensaje, emisor=emisor)\r\n"
    "    if usuario.email and '@' in usuario.email:\r\n"
    "        try:\r\n"
    "            send_mail(\r\n"
    "                subject=asunto,\r\n"
    "                message=mensaje,\r\n"
    "                from_email=django_settings.DEFAULT_FROM_EMAIL,\r\n"
    "                recipient_list=[usuario.email],\r\n"
    "                fail_silently=True,\r\n"
    "            )\r\n"
    "        except Exception:\r\n"
    "            pass\r\n"
    "\r\n"
    "\r\n"
    "def solo_admin(view_func):"
)
assert old0 in content, "NO ENCONTRADO: bloque 0"
content = content.replace(old0, new0, 1)
print("OK 0 - funcion auxiliar")

# ── 1. Admin pago crear ───────────────────────────────────────────────────────
old1 = (
    "            )\r\n"
    "            messages.success(request, 'Pago registrado correctamente.')\r\n"
    "            return admin_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/pagos/form.html', {"
)
new1 = (
    "            )\r\n"
    "            _notificar_pago(pago_obj, 'registrado', request.user)\r\n"
    "            messages.success(request, 'Pago registrado correctamente.')\r\n"
    "            return admin_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/pagos/form.html', {"
)
assert old1 in content, "NO ENCONTRADO: bloque 1"
content = content.replace(old1, new1, 1)
print("OK 1 - admin pago crear (pendiente notif)")

# Renombrar la variable en el create del admin
old1b = (
    "            Pago.objects.create(\r\n"
    "                jugador_id=jugador_id,\r\n"
    "                concepto=concepto,\r\n"
    "                descripcion=descripcion,\r\n"
    "                monto=monto_dec,\r\n"
    "                fecha_vencimiento=fecha_vencimiento,\r\n"
    "                fecha_pago=fecha_pago,\r\n"
    "                estado=estado,\r\n"
    "                metodo_pago=metodo_pago,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_pago(pago_obj, 'registrado', request.user)"
)
new1b = (
    "            pago_obj = Pago.objects.create(\r\n"
    "                jugador_id=jugador_id,\r\n"
    "                concepto=concepto,\r\n"
    "                descripcion=descripcion,\r\n"
    "                monto=monto_dec,\r\n"
    "                fecha_vencimiento=fecha_vencimiento,\r\n"
    "                fecha_pago=fecha_pago,\r\n"
    "                estado=estado,\r\n"
    "                metodo_pago=metodo_pago,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_pago(pago_obj, 'registrado', request.user)"
)
assert old1b in content, "NO ENCONTRADO: bloque 1b"
content = content.replace(old1b, new1b, 1)
print("OK 1b - admin pago crear (variable)")

# ── 2. Admin pago editar ──────────────────────────────────────────────────────
old2 = (
    "            messages.success(request, 'Pago actualizado correctamente.')\r\n"
    "            return admin_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/pagos/form.html', {\r\n"
    "        'titulo':    'E"
)
new2 = (
    "            _notificar_pago(pago, 'actualizado', request.user)\r\n"
    "            messages.success(request, 'Pago actualizado correctamente.')\r\n"
    "            return admin_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'panel/pagos/form.html', {\r\n"
    "        'titulo':    'E"
)
assert old2 in content, "NO ENCONTRADO: bloque 2"
content = content.replace(old2, new2, 1)
print("OK 2 - admin pago editar")

# ── 3. Admin marcar_pagado ────────────────────────────────────────────────────
old3 = (
    "    pago.save()\r\n"
    "    _crear_finanza_por_pago(pago, request.user)\r\n"
    "    messages.success(request, f'Pago de {pago.jugador.usuario.get_full_name() or pago.jugador.usuario.username} marcado como pagado.')\r\n"
    "    return admin_pagos_lista(request)"
)
new3 = (
    "    pago.save()\r\n"
    "    _crear_finanza_por_pago(pago, request.user)\r\n"
    "    _notificar_pago(pago, 'pagado', request.user)\r\n"
    "    messages.success(request, f'Pago de {pago.jugador.usuario.get_full_name() or pago.jugador.usuario.username} marcado como pagado.')\r\n"
    "    return admin_pagos_lista(request)"
)
assert old3 in content, "NO ENCONTRADO: bloque 3"
content = content.replace(old3, new3, 1)
print("OK 3 - admin marcar_pagado")

# ── 4. Entrenador pago crear ──────────────────────────────────────────────────
old4 = (
    "            messages.success(request, 'Pago registrado correctamente.')\r\n"
    "            return ent_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/pagos/form.html', {"
)
new4 = (
    "            _notificar_pago(pago_ent, 'registrado', request.user)\r\n"
    "            messages.success(request, 'Pago registrado correctamente.')\r\n"
    "            return ent_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/pagos/form.html', {"
)
assert old4 in content, "NO ENCONTRADO: bloque 4"
content = content.replace(old4, new4, 1)
print("OK 4 - entrenador pago crear (notif)")

# Renombrar variable en create del entrenador
old4b = (
    "            Pago.objects.create(\r\n"
    "                jugador_id=jugador_id,\r\n"
    "                concepto=concepto,\r\n"
    "                descripcion=descripcion,\r\n"
    "                monto=monto_dec,\r\n"
    "                fecha_vencimiento=fecha_vencimiento,\r\n"
    "                fecha_pago=fecha_pago,\r\n"
    "                estado=estado,\r\n"
    "                metodo_pago=metodo_pago,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_pago(pago_ent, 'registrado', request.user)"
)
new4b = (
    "            pago_ent = Pago.objects.create(\r\n"
    "                jugador_id=jugador_id,\r\n"
    "                concepto=concepto,\r\n"
    "                descripcion=descripcion,\r\n"
    "                monto=monto_dec,\r\n"
    "                fecha_vencimiento=fecha_vencimiento,\r\n"
    "                fecha_pago=fecha_pago,\r\n"
    "                estado=estado,\r\n"
    "                metodo_pago=metodo_pago,\r\n"
    "                registrado_por=request.user,\r\n"
    "            )\r\n"
    "            _notificar_pago(pago_ent, 'registrado', request.user)"
)
assert old4b in content, "NO ENCONTRADO: bloque 4b"
content = content.replace(old4b, new4b, 1)
print("OK 4b - entrenador pago crear (variable)")

# ── 5. Entrenador pago editar ─────────────────────────────────────────────────
old5 = (
    "            messages.success(request, 'Pago actualizado correctamente.')\r\n"
    "            return ent_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/pagos/form.html', {"
)
new5 = (
    "            _notificar_pago(pago, 'actualizado', request.user)\r\n"
    "            messages.success(request, 'Pago actualizado correctamente.')\r\n"
    "            return ent_pagos_lista(request)\r\n"
    "\r\n"
    "    return render(request, 'entrenador/pagos/form.html', {"
)
assert old5 in content, "NO ENCONTRADO: bloque 5"
content = content.replace(old5, new5, 1)
print("OK 5 - entrenador pago editar")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
