# -*- coding: utf-8 -*-
"""Mahjong_AI_V0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xaP_JAN75TlLQl5SbezGybYV5cD8VobG

import moudules
"""

import csv
import random
import math
import numpy as np
import pandas as pd
from enum import Enum

"""Enum of tiles"""

#🀀🀁🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣🀤🀥🀦🀧🀨🀩🀪🀫

class t(Enum):
  W1 = 11 #🀇
  W2 = 12 #🀈
  W3 = 13 #🀉
  W4 = 14 #🀊
  W5 = 15 #🀋
  W5R = 10 #🀋
  W6 = 16 #🀌
  W7 = 17 #🀍
  W8 = 18 #🀎
  W9 = 19 #🀏

  T1 = 21 #🀙
  T2 = 22 #🀚
  T3 = 23 #🀛
  T4 = 24 #🀜
  T5 = 25 #🀝
  T5R = 20 #🀋
  T6 = 26 #🀞
  T7 = 27 #🀟
  T8 = 28 #🀠
  T9 = 29 #🀡

  S1 = 31 #🀐
  S2 = 32 #🀑
  S3 = 33 #🀒
  S4 = 34 #🀓
  S5 = 35 #🀔
  S5R = 30 #🀋
  S6 = 36 #🀕
  S7 = 37 #🀖
  S8 = 38 #🀗
  S9 = 39 #🀘

  East = 1  #🀀
  South = 2  #🀁
  West = 3  #🀂
  North = 4  #🀃
  White = 5  #🀆
  Fa = 6  #🀅
  Zhong = 7  #🀄

hand_tiles=[] #手牌
hand_tiles = [t.W2, t.W2, t.W2, t.W6, t.W7, t.W8, t.T3, t.T4, t.T5, t.S1, t.S4, t.S5, t.S9, t.S2] #example

dora_tiles = [] #寶牌
dora_tiles = [t.W3] #example

my_river = [] #我的棄牌堆
my_river = [t.West] #example

upper_river = [] #上家棄牌堆
upper_river = [t.South, t.East] #example

lower_river = [] #下家棄牌堆
lower_river = [t.Fa, t.North] #example

across_river = [] #對家棄牌堆
across_river = [t.T1, t.North] #example


remain_tiles = {
    t.W1: 4,
    t.W2: 4,
    t.W3: 4,
    t.W4: 4,
    t.W5: 4,
    t.W5R: 4,
    t.W6: 4,
    t.W7: 4,
    t.W8: 4,
    t.W9: 4,

    t.T1: 4,
    t.T2: 4,
    t.T3: 4,
    t.T4: 4,
    t.T5: 4,
    t.T5R: 4,
    t.T6: 4,
    t.T7: 4,
    t.T8: 4,
    t.T9: 4,

    t.S1: 4,
    t.S2: 4,
    t.S3: 4,
    t.S4: 4,
    t.S5: 4,
    t.S5R: 4,
    t.S6: 4,
    t.S7: 4,
    t.S8: 4,
    t.S9: 4,

    t.East : 4,
    t.South : 4,
    t.West : 4,
    t.North : 4,
    t.White : 4,
    t.Fa : 4,
    t.Zhong : 4
} #全場剩餘牌

tile_pos = random.randint(1,14)
tile_name = hand_tiles[tile_pos]

decision = (tile_pos, tile_name.name)
print(decision)