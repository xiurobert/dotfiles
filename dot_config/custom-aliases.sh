#!/bin/bash
alias vim='nvim'
alias pbcopy="xclip -sel clip"
alias py="python"
complete -F _python py
alias ipy="ipython"
alias refreshenv="source ~/.bashrc"

alias tail_qtile_log="tail -f $HOME/.local/share/qtile/qtile.log"

alias install-pytorch="pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116"
alias clean-pytorch="pip3 uninstall torch torchvision torchaudio --yes"
alias clean-inst-pytorch="clean-pytorch && install-pytorch"

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
