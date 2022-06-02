#!/bin/bash
alias pbcopy="xclip -sel clip"

function _df_upd_helper() {
    git add -A
    git commit -am "changed some stuff (commited via bash alias)"
    git push
}

function dotfile_update() {
    chezmoi re-add
    cd $(chezmoi source-path) && _df_upd_helper
}
