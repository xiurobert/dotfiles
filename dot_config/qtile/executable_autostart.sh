#!/bin/sh
xwallpaper --center "$HOME"/wallpapers/mojave-day.jpg &
picom -b & 
xrandr --output DP-4 --mode 3440x1440 --rate 100 &
exec nm-applet &
exec volctl &
