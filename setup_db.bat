@echo off
echo ========================================
echo CONFIGURACION DE POSTGRESQL PARA DEPORTES
echo ========================================
echo.

echo Ejecutando configuracion de base de datos...
echo Nota: Se te pedira la contraseña del usuario 'postgres'
echo.

psql -U postgres -f setup_postgresql.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo CONFIGURACION COMPLETADA EXITOSAMENTE
    echo ========================================
    echo.
    echo Base de datos: deportes_db
    echo Usuario: deportes_user
    echo Contraseña: Deportes123
    echo Host: localhost
    echo Puerto: 5432
    echo.
    echo Ahora puedes ejecutar:
    echo python manage.py makemigrations
    echo python manage.py migrate
    echo python manage.py create_test_users
    echo python manage.py runserver
) else (
    echo.
    echo ========================================
    echo ERROR EN LA CONFIGURACION
    echo ========================================
    echo.
    echo Verifica que PostgreSQL este instalado y ejecutandose
    echo Verifica que el usuario 'postgres' tenga contraseña configurada
)

pause