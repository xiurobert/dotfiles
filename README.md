# archsys

Dotfiles for my arch box

Ansible playbook coming soon

## Installation commands

```bash
sudo pacman -S git vim htop openssh
sudo pacman -S vlc firefox discord
sudo pacman -S gnome-keyring
sudo pacman -S alacritty qtile cezmoi xwallpaper rofi lightdm lightdm-slick-greeter picom xclip
# make sure to change the greeter
# https://wiki.archlinux.org/title/LightDM#Greeter
sudo systemctl enable lightdm
sudo pacman -S powerline
sudo pacman -S python-pip
pip install psutil
``` 

### Post-install

Fix mouse acceleration

Edit: `/etc/X11/xorg.conf.d/50-mouse-acceleration.conf`

Or curl this: https://gist.githubusercontent.com/xiurobert/78b3552d301568ca8572545898b2a577/raw/ed5a1a2dcdb0fd1bc41bac643d1117b9ebf87eb1/50-mouse-acceleration.conf

```
Section "InputClass"
    Identifier "Logitech catchall"
    MatchIsPointer "yes"
    Option "AccelerationProfile" "-1"
    Option "AccelerationScheme" "none"
    Option "AccelSpeed" "-1"
EndSection
```
