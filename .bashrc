#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

eval "$(starship init bash)"
alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '
alias please='sudo'
alias fuck='sudo !!'
alias vpn_on='wg-quick up northernblow'
alias vpn_off='wg-quick down northernblow'
alias hy='Hyprland'
alias off='poweroff'
alias nv='nvim'
export DOCKER_HOST=unix:///var/run/docker.sock
