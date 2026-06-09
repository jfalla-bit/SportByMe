data = open('config/settings.py', 'rb').read()
old = b"EMAIL_HOST_USER     = 'tucorreo@gmail.com'      # <-- cambia esto\r\nEMAIL_HOST_PASSWORD = 'tu_contrasena_de_app'    # <-- cambia esto"
new = b"EMAIL_USE_SSL       = False\r\nEMAIL_HOST_USER     = config('EMAIL_HOST_USER')\r\nEMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')"
if old in data:
    data = data.replace(old, new)
    open('config/settings.py', 'wb').write(data)
    print('OK - reemplazado')
else:
    print('NO ENCONTRADO')
    # buscar variante con espacios distintos
    import re
    text = data.decode('utf-8', errors='replace')
    print(repr([l for l in text.splitlines() if 'EMAIL_HOST_USER' in l or 'EMAIL_HOST_PASSWORD' in l]))
