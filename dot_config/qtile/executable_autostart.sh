#!/bin/sh
xwallpaper --center "$HOME"/wallpapers/mojave-day.jpg &
picom -b &
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }" &
xrandr --output DP-2 --mode 3440x1440 --rate 100 &
exec nm-applet &
exec volctl &
exec solaar &
