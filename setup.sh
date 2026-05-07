#!/bin/bash

echo "Actualizando paquetes del sistema..."
sudo yum update -y

echo "Instalando paquetes esenciales..."
sudo yum install -y git vim docker python3 python3-pip

echo "Iniciando servicio Docker..."
sudo service docker start

echo "Instalando dependencias de Python..."
pip3 install --user boto3

echo "Verificando versiones instaladas..."
git --version
vim --version | head -n 1
docker --version
python3 --version
pip3 show boto3

echo "Configuración del entorno completada correctamente."
