#!/bin/bash

CYAN='\033[36m'
NC='\033[0m'

echo -e "${CYAN}Actualizando Mirrors${NC}"
echo ""

sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
sudo reflector --verbose --latest 10 --protocol https --sort rate --save /etc/pacman.d/mirrorlist

echo -e "${CYAN}Actualizando paquetes PACMAN${NC}"
echo ""

sudo pacman -Syu 

echo -e "${CYAN}Actualizando paquetes AUR${NC}"
echo ""

paru 

echo -e "${CYAN}Actualizando paquetes FLATPAK${NC}"
echo ""

flatpak update 

echo -e "${CYAN}Eliminando paquetes huerfanos${NC}"
echo ""

sudo pacman -Rsc $(pacman -Qtdq) --noconfirm

echo -e "${CYAN}Borrando CACHE${NC}"
echo ""

sudo pacman -Sc --noconfirm

echo -e "${CYAN}Preciona ENTER para salir${NC}"
read -p ""