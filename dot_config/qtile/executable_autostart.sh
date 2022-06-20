#!/bin/sh
xwallpaper --center "$HOME"/wallpapers/mojave-day.jpg &
picom -b & 
xrandr --output DP-2 --mode 3440x1440 --rate 100 &
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }" &
exec nm-applet &
exec volctl &
exec solaar &
