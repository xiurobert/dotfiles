#!/bin/sh
xwallpaper --center "$HOME"/wallpapers/mojave-day.jpg &
picom -b & 
xrandr --output HDMI-0 --mode 3440x1440 --rate 100 &
exec volctl &
