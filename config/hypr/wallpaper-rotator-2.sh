#!/bin/bash

# Setea la ruta al directorio de fondos de pantalla
wallpapersDir="/home/chie/wallpaper"

# Obtiene una lista de todos los archivos de imagen en el directorio de fondos de pantalla
wallpapers=("$wallpapersDir"/*)

# Espera 3 segundo antes de iniciar
sleep 5

# Inicia un bucle infinito
while true; do
    # Chequea si el array de wallpapers está vacío
    if [ ${#wallpapers[@]} -eq 0 ]; then
        # Si el array está vacío, rellénalo con los archivos de imagen
        wallpapers=("$wallpapersDir"/*)
    fi

    # Selecciona un fondo de pantalla aleatorio del array
    wallpaperIndex=$(( RANDOM % ${#wallpapers[@]} ))
    selectedWallpaper="${wallpapers[$wallpaperIndex]}"

    # Actualiza el fondo de pantalla usando el comando swww img
    swww img "$selectedWallpaper" --resize stretch --transition-type any --transition-duration 1 --outputs DP-1

    # Remueve el fondo de pantalla seleccionado del array
    unset "wallpapers[$wallpaperIndex]"

    # Elimina cache 
    swww clear-cache

    # Espera antes de seleccionar el siguiente fondo de pantalla
    sleep 295
done