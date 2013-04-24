remote_run
==========

Toolset is designed to simplify developing process when
you should often perform some actions on remote server but want to edit files locally.
Tool will be helpful for different serverside developers.
Using this tool you can edit code in your preferable IDE (QtCreator, Sublime, Gvim, etc)
but easily run compiler on server whith custom build environment.


System requirements
==================
Your local should be able to run python3 scripts and have rsync tool
(it is sertanly available for MacOs, Linux and other Unix-like systems).
Your remote server should be accesseible through rsync and ssh.

Toolset is tested now on MacOS but should work on other Unix-like systems.

Quick start
===========

- Go to your home directory:

  cd

- Get latest copy of toolset:

  git clone git://github.com/golovasteek/remote_run.git

- Add toolset dir to your PATH environment variable. For example add to yor ~/.bashrc file line 

  export PATH+=~/remote_run:$PATH

- Got to your project dir and configure remote run there:

  rr --init

- Set up congigure wariables with your prefrable server and directory on server.

- Run compiler on server

  rr gcc hello.cpp -o hello
