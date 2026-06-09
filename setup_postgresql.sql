-- Script para configurar PostgreSQL para el proyecto deportes
-- Ejecutar como superusuario de PostgreSQL (postgres)

-- Crear usuario
CREATE USER deportes_user WITH PASSWORD 'Deportes123';

-- Crear base de datos
CREATE DATABASE deportes_db OWNER deportes_user;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE deportes_db TO deportes_user;

-- Conectar a la base de datos deportes_db
\c deportes_db

-- Otorgar permisos en el esquema public
GRANT ALL ON SCHEMA public TO deportes_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO deportes_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO deportes_user;

-- Configurar permisos por defecto para objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO deportes_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO deportes_user;