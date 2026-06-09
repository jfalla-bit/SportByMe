with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

old = (
    "def admin_notificaciones_leer_todos(request):\r\n"
    "    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)\r\n"
    "    return HttpResponseRedirect('/panel/notificaciones/')\r\n"
    "\r\n"
    "\r\n"
    "@so"
)
new = (
    "def admin_notificaciones_leer_todos(request):\r\n"
    "    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)\r\n"
    "    return HttpResponseRedirect('/panel/notificaciones/')\r\n"
    "\r\n"
    "\r\n"
    "@solo_admin\r\n"
    "def admin_notificacion_eliminar(request, noti_id):\r\n"
    "    \"\"\"Eliminar una notificacion propia del administrador.\"\"\"\r\n"
    "    noti = get_object_or_404(Notificacion, id=noti_id, usuario=request.user)\r\n"
    "    noti.delete()\r\n"
    "    messages.success(request, 'Notificacion eliminada.')\r\n"
    "    return HttpResponseRedirect('/panel/notificaciones/')\r\n"
    "\r\n"
    "\r\n"
    "@solo_entrenador\r\n"
    "def ent_notificacion_eliminar(request, noti_id):\r\n"
    "    \"\"\"Eliminar una notificacion propia del entrenador.\"\"\"\r\n"
    "    noti = get_object_or_404(Notificacion, id=noti_id, usuario=request.user)\r\n"
    "    noti.delete()\r\n"
    "    messages.success(request, 'Notificacion eliminada.')\r\n"
    "    return HttpResponseRedirect('/entrenador/mensajes/')\r\n"
    "\r\n"
    "\r\n"
    "@solo_deportista\r\n"
    "def dep_notificacion_eliminar(request, noti_id):\r\n"
    "    \"\"\"Eliminar una notificacion propia del deportista.\"\"\"\r\n"
    "    noti = get_object_or_404(Notificacion, id=noti_id, usuario=request.user)\r\n"
    "    noti.delete()\r\n"
    "    messages.success(request, 'Notificacion eliminada.')\r\n"
    "    return HttpResponseRedirect('/deportista/mensajes/')\r\n"
    "\r\n"
    "\r\n"
    "@so"
)

assert old in content, "NO ENCONTRADO"
content = content.replace(old, new, 1)
print("OK - vistas eliminar")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
