#!/bin/bash

# Executes within xterm script installed system-wide.

# sudo apt-get update;
# sudo apt-get upgrade -y;
cd ~/Documents/projects/Bingo;
source bingoenv/bin/activate;
cd bingo;
python manage.py test;
gulp;
