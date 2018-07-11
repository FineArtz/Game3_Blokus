@echo off
start env.bat
:loop
    player.py < envout.txt > playerout.txt
    player.py < envout.txt > playerout.txt
    goto loop