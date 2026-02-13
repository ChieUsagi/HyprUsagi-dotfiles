#!/bin/bash

echo -e "\e[1;32m==>\e[0m \e[1mBuscando actualizaciones...\e[0m"
echo ""

# Actualizar espejo usando Reflector
#sudo reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist

# Actualizar la base de datos de pacman
#sudo pacman -Syy

echo -e "\e[1;32m==>\e[0m \e[1mPresione "Enter" para salir...\e[0m"
read -p ""
exit