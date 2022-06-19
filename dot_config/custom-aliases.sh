#!/bin/bash
alias pbcopy="xclip -sel clip"
alias py="python"
complete -F _python py
alias ipy="ipython"

alias tail_qtile_log="tail -f $HOME/.local/share/qtile/qtile.log"

function _df_upd_helper() {
    git add -A
    git commit -am "updated dotfiles without description (commit via dotfile_update)"
    git push
}

function dotfile_update() {
    chezmoi re-add
    curr_dir=$(pwd)
    cd "$(chezmoi source-path)" && _df_upd_helper
    cd "$curr_dir" || exit
}
