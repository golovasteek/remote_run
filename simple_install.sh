#!/usr/bin/env bash -x

PWD=$(pwd)

SCRIPT_NAME="$0"
SCRIPT_DIR=$(dirname $(realpath "$SCRIPT_NAME"))

BIN_DIR=${1:-"$HOME/bin"}

FILES="rr make"
RCFILE_NAME="$HOME/.remoterunrc" 

function make_links()
{
    for f in $FILES ; do 
        ln -ns "$SCRIPT_DIR/$f" "$BIN_DIR/" 
    done
}

function remove_links()
{
    for f in $FILES ; do 
        rm -f  "$BIN_DIR/$f" 
    done
}

remove_links
make_links

cp "$SCRIPT_DIR/remoterunrc.default" "$RCFILE_NAME"
vi "$RCFILE_NAME"
