Remote Run
==========

Toolset is designed to simplify developing process when
you should often perform some actions on remote server but want to edit files locally.
Tool will be helpful for different serverside developers.
Using this tool you can edit code in your preferable editor or IDE (QtCreator, Sublime, Gvim, etc)
but easily run compiler on server whith custom build environment.


System requirements
==================
Your local should be able to run python3 scripts and have rsync tool
(it is sertanly available for Linux, OS X and other Unix-like systems).
Your remote server should be accesseible through rsync and ssh.

Toolset is tested now on OS X but should work on other Unix-like systems.

Quick start
===========

- Get latest copy of toolset:

    ```bash
    mkdir -p ~/bin
    git clone git://github.com/golovasteek/remote_run.git ~/bin/remote_run
    ln -s ~/bin/remote_run/rr.py ~/bin/rr
    ```
    If ~/bin is not in your $PATH you can add it:
    ```bash
    echo "export PATH+=\"~/bin:\$PATH\" >> ~/.bashrc
    . ~/.bashrc
    ```

- Go to your project dir and configure remote run there:

    ```bash
    rr --init
    ```

    Editor will open. Set up configure wariables with your prefrable server and directory on server.

- Run your commands on server. Example:

    ```bash
    rr gcc hello.cpp -o hello
    ```
    Or launch shell:
    ```bash
    rr
    ```

