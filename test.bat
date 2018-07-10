@echo off
environment.py > envout.txt
:loop
    player.py < envout.txt > playerout.txt
    environment.py < playerout.txt
    player.py < envout.txt > playerout.txt
    environment.py < playerout.txt
    goto loop