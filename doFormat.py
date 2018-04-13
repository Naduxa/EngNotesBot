#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
import telebot
import json
from threading import Thread, Lock

dataDir_path = 'dataDir/dictionary/'
lines = []
with open(dataDir_path + 'ENRUS.TXT', 'rw') as f:
    for l in f:
        lines.append(l)

with open(dataDir_path + 'ENRUS2.txt', 'a') as f:
    for i, l in enumerate(lines):
        if i % 2 == 0:
            f.write(l.strip() + ' - ' + lines[i + 1].strip() + '\n')