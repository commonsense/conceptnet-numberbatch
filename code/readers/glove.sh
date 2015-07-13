#!/bin/sh

if [[ $# -eq 0 ]] ; then
    echo 'Usage: glove.sh [glove-file] [label-file] [vector-file]'
    exit 0
fi

cut -d" " -f1 $1 >$2
cut -d" " -f2- $1 | python glove.py $(wc -l $1) $3
