<h1 align="center">
HyprUsagi - Dotfiles

## 

  * 
    ````
    pacman -S pipewire wireplumber pipewire-pulse pipewire-alsa
    
    systemctl --user enable pipewire wireplumber pipewire-pulse pipewire-alsa
    ````
  * 
    `/etc/mkinitcpio.comf`
    
    ````
    mkinitcpio -p linux
    ````
  * 
    `/etc/default/grub`
    
    ````
    grub-mkconfig /boot/grub/grub.cfg
    ````
  * 
    `/etc/sudoers`

    ````
    Defaults env_reset,pwfeedback
    ````
    

## Primera instalacion

  * Paquetes basicos:

    ````
    sudo pacman -S firefox kitty zsh git curl fastfetch flatpack plymouth
    ````

  * Chaotic AUR:
    ````
    sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
    sudo pacman-key --lsign-key 3056513887B78AEB
    ````
    ````
    sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
    sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
    ````
    
    Agregar al final del archivo `/etc/pacman.conf`:
    
    ````
    [chaotic-aur]
    Include = /etc/pacman.d/chaotic-mirrorlist
    ````
    
    > en el archivo `/etc/pacman.conf` tambien habilitar `Colors` y agregar `ILoveCandy`
    
    ````
    sudo pacman -Syu
    ````
    ````
    sudo pacman -S pamac
    ````
    
  * Flathub Remote:
   
    ````
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    ````

  * Paru AUR Helper:

    ````
    sudo pacman -S --needed base-devel
    git clone https://aur.archlinux.org/paru.git
    cd paru
    makepkg -si
    ````

  * Nyarch Updater:

    ````
    cd /tmp
    wget https://github.com/nyarchlinux/nyarchupdater/releases/latest/download/nyarchupdater.flatpak
    flatpak install nyarchupdater.flatpak
    ````

  * Nyarch Script:

    ````
    cd /tmp
    wget https://github.com/nyarchlinux/nyarchscript/releases/latest/download/nyarchscript.flatpak
    flatpak install nyarchscript.flatpak
    ````

## Oh My ZSH

  * Instalacion:

    ````
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ````

  * Plugins:

    ````
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    ````
    ````
    git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search
    ````
  
  * En el archivo `~/.zshrc` cambiar:

    ````
    plugins=(git zsh-syntax-highlighting zsh-history-substring-search)
    ````
    ````
    ZSH_THEME="awesomepanda"
    ````
    
    Al final agregar:
    
    ````
    PROMPT='%F{cyan}%n%f_%F{cyan}%m %F{green}%~ %F{magenta}> '
    ````

## Paquetes necesarios
 
   ````
   sudo pacman-S waybar swaync swayosd polkit-gnome noto-fonts ttf-jetbrains-mono-nerd swwww nwg-drawer clipse hypridle hyprlock flameshot power-profiles-daemon pavucontrol gamemode pacman-contrib reflector
   ````
