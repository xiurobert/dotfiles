# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.backend.base import Window
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import libqtile

from libqtile.log_utils import logger

from collections import namedtuple

mod = "mod4"
alt = "mod1"

terminal = guess_terminal()
browser = "firefox"
file_manager = "pcmanfm"


@lazy.function
def update_volume(qtile: libqtile.qtile):
    # logger.warn("Triggering the poll")
    w = qtile.widgets_map["volume"]
    # logger.warn(w)
    w.poll()


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file browser"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "r", lazy.spawn('rofi -show combi'), desc="Opens rofi"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), update_volume(), desc="Toggle mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 1"), update_volume()),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 1"), update_volume())
]

groups = [
    Group("1", label="www", layout="columns"),
    Group("2", label="dev", layout="monadtall"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                desc=f"Move focused window to group {i.name}",
            ),
        ]
    )


class Colors:
    SIERRA_BLUE = "#69abce"


class StandardColors:
    WHITE = "#ffffff"
    BLACK = "#000000"
    MAGENTA = "#ff00ff"
    LIGHT_GRAY = "#d3d3d3"
    DARK_GRAY = "#a9a9a9"
    DARK_CYAN = "#004c44"
    CYAN = "#00ffff"


nv_green = "76B900"

layouts = [
    layout.Columns(border_focus=StandardColors.CYAN, border_normal=StandardColors.DARK_CYAN,
                   border_width=1, margin=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(border_focus=StandardColors.CYAN, border_normal=StandardColors.DARK_CYAN,
                     border_width=1, margin=4, ratio=0.65),
    layout.MonadThreeCol(border_focus=StandardColors.CYAN, border_normal=StandardColors.DARK_CYAN,
                         border_width=1, margin=4,
                         new_client_position='bottom'),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def gen_sep(from_color: str, to_color: str):
    """
    Generates a powerline-style seperator.

    :param from_color: The color of the seperator. Usually the background of your previous element.
    :param to_color: The color of the next element. Typically, the background of your next element.
    :return: widget.TextBox
    """
    return widget.TextBox(
        text="", foreground=from_color, background=to_color, fontsize=30, font="JetBrains Mono", padding=0
    )


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(highlight_method='line', font="Sans"),
                widget.WindowName(font="Sans"),

                gen_sep(StandardColors.DARK_CYAN, StandardColors.BLACK),
                widget.TextBox(text="", font="Font Awesome 6 Free", background=StandardColors.DARK_CYAN),
                widget.DF(visible_on_warn=False,
                          format='{f}{m}/{s}{m}',
                          update_interval=60, partition="/home", background=StandardColors.DARK_CYAN),
                widget.Spacer(length=10, background=StandardColors.DARK_CYAN),

                gen_sep(Colors.SIERRA_BLUE, StandardColors.DARK_CYAN),
                widget.Net(background=Colors.SIERRA_BLUE),
                widget.Spacer(length=10, background=Colors.SIERRA_BLUE),

                gen_sep(StandardColors.LIGHT_GRAY, Colors.SIERRA_BLUE),
                widget.PulseVolume(name='volume',
                                   get_volume_command="pamixer --get-volume",
                                   mute_command="pamixer -t",
                                   foreground=StandardColors.BLACK,
                                   background=StandardColors.LIGHT_GRAY),
                widget.Spacer(length=5, background=StandardColors.LIGHT_GRAY),

                gen_sep('a87b32', StandardColors.LIGHT_GRAY),
                widget.CPU(background='a87b32'),
                widget.Spacer(length=10, background='a87b32'),

                gen_sep(StandardColors.MAGENTA, 'a87b32'),
                widget.TextBox(text="", font="Font Awesome 6 Free",
                               background=StandardColors.MAGENTA),
                widget.Memory(format='{MemUsed:.2f}{mm}/{MemTotal:.2f}{mm}', measure_mem='G',
                              background=StandardColors.MAGENTA),
                widget.Spacer(length=10, background=StandardColors.MAGENTA),

                gen_sep("0071C5", StandardColors.MAGENTA),
                widget.TextBox(text="", font="Font Awesome 6 Free", background="0071C5"),
                widget.ThermalSensor(background="0071C5", tag_sensor="Package id 0"),

                gen_sep(nv_green, "0071C5"),
                widget.Image(filename="~/.config/qtile/icons/gpu.png", background=nv_green),
                widget.NvidiaSensors(background=nv_green, foreground=StandardColors.WHITE),

                gen_sep(StandardColors.WHITE, nv_green),
                widget.Systray(background=StandardColors.WHITE),
                widget.Spacer(length=10, background=StandardColors.WHITE),

                gen_sep(StandardColors.DARK_GRAY, StandardColors.WHITE),
                widget.Clock(format="%I:%M %p", font="Sans",
                             foreground=StandardColors.BLACK,
                             background=StandardColors.DARK_GRAY),
                widget.Spacer(length=10, background=StandardColors.DARK_GRAY),

                widget.QuickExit(),
            ],
            24,
            border_width=[1] * 4,
            border_color=[Colors.SIERRA_BLUE] * 4
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


# Autostart rules
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


# @hook.subscribe.client_new
# def client_new(client: Window):
#     if "Firefox".lower() in client.name.lower():
#         client.togroup("1")

ides = ["jetbrains-pycharm-ce", "jetbrains-pycharm"]


@hook.subscribe.client_managed
def ides_to_dev(client: Window):
    # logger.warning(client.get_wm_class())
    if client.get_wm_class()[1] in ides:
        client.togroup("2", switch_group=True)
        # client.cmd_bring_to_front()


@hook.subscribe.client_managed
def vscode_to_dev(client: Window):
    # dev = groups[1]
    # logger.warn(dev.layout_opts)
    if client.get_wm_class()[1] == "Code":
        client.togroup("2", switch_group=True)
