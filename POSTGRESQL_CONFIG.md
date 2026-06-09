# CONFIGURACIÓN DE POSTGRESQL PARA PROYECTO DEPORTES

## Información de Conexión
- **Base de datos:** deportes_db
- **Usuario:** deportes_user  
- **Contraseña:** Deportes123
- **Host:** localhost
- **Puerto:** 5432

## Cadena de Conexión
```
postgresql://deportes_user:Deportes123@localhost:5432/deportes_db
```

## Comandos para Conectarse

### psql (Línea de comandos)
```bash
psql -h localhost -p 5432 -U deportes_user -d deportes_db
```

### pgAdmin 4 (Interfaz gráfica)
1. Host: localhost
2. Puerto: 5432
3. Base de datos: deportes_db
4. Usuario: deportes_user
5. Contraseña: Deportes123

### DBeaver (Multiplataforma)
1. Tipo: PostgreSQL
2. Host: localhost
3. Puerto: 5432
4. Base de datos: deportes_db
5. Usuario: deportes_user
6. Contraseña: Deportes123

## Comandos SQL Útiles
```sql
-- Ver todas las tablas
\dt

-- Describir tabla
\d nombre_tabla

-- Ver usuarios
SELECT * FROM users;

-- Salir
\q
```