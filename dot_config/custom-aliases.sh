#!/bin/bash
alias pbcopy="xclip -sel clip"

function _df_upd_helper() {
    git add -A
    git commit -am "changed some stuff (committed via bash alias)"
    git push
}

function dotfile_update() {
    chezmoi re-add
    curr_dir=$(pwd)
    echo "$curr_dir"
    cd "$(chezmoi source-path)" && _df_upd_helper
    cd curr_dir || exit
}
