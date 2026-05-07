#!/bin/bash

echo "Creando grupo devops..."
sudo groupadd devops 2>/dev/null || echo "El grupo devops ya existe."

echo "Creando usuario devops_user..."
sudo useradd -m -s /bin/bash -G devops devops_user 2>/dev/null || echo "El usuario devops_user ya existe."

echo "Asignando permisos sobre la carpeta ~/environment..."
sudo chown -R devops_user:devops ~/environment

echo "Mostrando información del usuario..."
id devops_user

echo "Restaurando permisos para ec2-user en ~/environment..."
sudo chown -R ec2-user:ec2-user ~/environment

echo "Gestión de usuarios y permisos completada."
