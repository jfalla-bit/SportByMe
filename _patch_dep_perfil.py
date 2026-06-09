with open('core/views.py', 'rb') as f:
    content = f.read().decode('utf-8')

old = (
    "    if request.method == 'POST':\r\n"
    "        first_name = request.POST.get('first_name', '').strip()\r\n"
    "        last_name  = request.POST.get('last_name', '').strip()\r\n"
    "        phone      = request.POST.get('phone', '').strip()\r\n"
    "        birth_date = request.POST.get('birth_date', '').strip() or None\r\n"
    "        email      = request.POST.get('email', '').strip()\r\n"
    "\r\n"
    "        # Validar email \u00fanico (excluyendo el propio)\r\n"
    "        if email and UserModel.objects.filter(\r\n"
    "                email__iexact=email).exclude(id=usuario.id).exists():\r\n"
    "            messages.error(request, f'El correo \"{email}\" ya est\u00e1 en uso por otra cuenta.')\r\n"
    "        else:\r\n"
    "            usuario.first_name = first_name\r\n"
    "            usuario.last_name  = last_name\r\n"
    "            usuario.phone      = phone\r\n"
    "            usuario.birth_date = birth_date\r\n"
    "            if email:\r\n"
    "                usuario.email = email\r\n"
    "            usuario.save()\r\n"
    "            messages.success(request, 'Perfil actualizado correctamente.')"
)
new = (
    "    if request.method == 'POST':\r\n"
    "        phone = request.POST.get('phone', '').strip()\r\n"
    "        email = request.POST.get('email', '').strip()\r\n"
    "\r\n"
    "        errores = []\r\n"
    "        import re\r\n"
    "        if phone and not re.match(r'^\\d{7,15}$', phone):\r\n"
    "            errores.append('El tel\u00e9fono debe contener solo n\u00fameros (7-15 d\u00edgitos).')\r\n"
    "        if email and UserModel.objects.filter(\r\n"
    "                email__iexact=email).exclude(id=usuario.id).exists():\r\n"
    "            errores.append(f'El correo \"{email}\" ya est\u00e1 en uso por otra cuenta.')\r\n"
    "\r\n"
    "        if errores:\r\n"
    "            for e in errores:\r\n"
    "                messages.error(request, e)\r\n"
    "        else:\r\n"
    "            usuario.phone = phone\r\n"
    "            if email:\r\n"
    "                usuario.email = email\r\n"
    "            usuario.save()\r\n"
    "            messages.success(request, 'Datos de contacto actualizados correctamente.')"
)

assert old in content, "NO ENCONTRADO"
content = content.replace(old, new, 1)
print("OK")

with open('core/views.py', 'wb') as f:
    f.write(content.encode('utf-8'))

print("DONE")
