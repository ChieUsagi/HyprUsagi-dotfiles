#!/bin/bash

# 1. Actualizar repositorios y paquetes
echo -e "\e[1;32m==>\e[0m \e[1mBuscando actualizaciones...\e[0m"
echo ""

UPDATES=$(checkupdates)
UPDATESFLAT=$(flatpak remote-ls --updates)

if [ -z "$UPDATES" ]; then
    echo -e "\e[1;36m>\e[0m \e[1mNo hay actualizaciones pacman disponibles\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1mActualizaciones pacman disponibles\e[0m"
    echo ""
    echo "$UPDATES"
    echo ""
    sudo pacman -Syu
    paru -Syu
fi

if [ -z "$UPDATESFLAT" ]; then
    echo -e "\e[1;36m>\e[0m \e[1mNo hay actualizaciones flatpak disponibles\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1mActualizaciones flatpak disponible\e[0m"
    echo ""
    echo "$UPDATESFLAT"
    echo ""
    sudo flatpak update
fi

# 2. Eliminar paquetes huerfanos
echo -e "\e[1;32m==>\e[0m \e[1mBuscando paquetes huerfanos...\e[0m"
echo ""

HUERFANOS=$(pacman -Qdt)

if [ -z "$HUERFANOS" ]; then
    echo -e "\e[1;36m>\e[0m \e[1mNo se encontraron paquetes huerfanos\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1mPaquetes huerfanos encontrados\e[0m"
    echo ""
    echo "$HUERFANOS"
    sudo pacman -Rns $(pacman -Qdtq) --noconfirm
fi

# 3. Eliminar paquetes flatpak no usados
echo -e "\e[1;32m==>\e[0m \e[1mBuscando paquetes flatpak no usados...\e[0m"
echo ""

UNUSEDFLAT=$(flatpak uninstall --unused)

if [ "$UNUSEDFLAT" == "Nada sin usar que desinstalar" ]; then
    echo -e "\e[1;36m>\e[0m \e[1mNo se encontraron paquetes flatpak sin usar\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1mPaquetes faltpak no usados\e[0m"
    echo ""
    echo "$UNUSEDFLAT"
    sudo flatpak uninstall --unused --delete-data
fi

# 4. Limpiar caché de pacman (paquetes obsoletos)
echo -e "\e[1;32m==>\e[0m \e[1mLimpiando caché...\e[0m"
echo ""

ODLCACHE=$(paccache -dk2)
UNINSTALLCACHE=$(paccache -duk0)

if [ "$ODLCACHE" == "[1m[32m==>(B[m[1m no candidate packages found for pruning(B[m" ]; then
    echo -e "\e[1;36m>\e[0m \e[1;mNo se encontraron versiones antiguas\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1;mVersiones antiguas encontradas\e[0m"
    echo ""
    echo "$ODLCACHE"
    sudo paccache -rk2
fi

if [ "$UNINSTALLCACHE" == "[1m[32m==>(B[m[1m no candidate packages found for pruning(B[m" ]; then
    echo -e "\e[1;36m>\e[0m \e[1;mNo se encontraron paquetes desinstalados\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1;mPaquetes desinstalados encontrados\e[0m"
    echo ""
    echo "$UNINSTALLCACHE"
    sudo paccache -ruk0
fi

# 5. Buscar archivos pacnew
echo -e "\e[1;32m==>\e[0m \e[1mBuscando archivos pacnew...\e[0m"
echo ""

PACNEW=$(pacdiff)

if [ -z "$PACNEW" ]; then
    echo -e "\e[1;36m>\e[0m \e[1mNo se encontraron archivos pacnew\e[0m"
    echo ""
else
    echo -e "\e[1;36m>\e[0m \e[1mArchivos pacnew encontrados\e[0m"
    echo ""
    echo "$PACNEW"
    sudo pacdiff
fi

echo -e "\e[1;32m==>\e[0m \e[1mPresione "Enter" para salir...\e[0m"
read -p ""
exit