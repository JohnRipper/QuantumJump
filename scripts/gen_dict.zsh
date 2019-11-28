#!/usr/bin/env zsh
# FAUX IS BAE

if ((# == 0)); then
    echo 'Generate a Python-ish dict, pass a range of unicode characters\nie a..z (case sensitive)\n\nUsage: ./gen_dict.zsh A..Z 🅰..🆉\n'
    exit 1
fi
a=({$1});
b=({$2});
for i in {1..$#a};
    echo \'$a[$i]\': \'$b[$i]\',
