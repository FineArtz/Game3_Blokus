Game 3: Blokus
======

Judge可分别调用environment.py和player.py进行交互。

environment.py:
------

* -p level: 人机对战，人为0号玩家。“level”代表AI的等级。

* -c level1 level2: 两AI对战，前者为0号玩家。“level1”和“level2”分别代表两AI的等级。

    -p和-c不能同时出现。
    
    默认-c 0 0
    
* -s x: 指定x号玩家先行。

    默认-s 0

player.py:
------

* -l level: 指定AI玩家的等级。

    默认-l 0
    
* -w w1 w2: 设置估价函数的权值。

    默认-w 20 10

