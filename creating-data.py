# -*- coding: utf-8 -*-
"""
rotina para criar dados a serem plotados e analisados

"""
import numpy as np
import os 
from os import listdir
from os.path import join
import pandas as pd
import math
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import fileinput
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable
from windrose import WindroseAxes
import random

lengthData = 4465 # tamanho do dado a ser criado: equivale a 30 dias de 10 em 10 min
quantSpike = 150 # quantidades de spikes

indexSpike = [random.randint(0, lengthData) for _ in range(quantSpike)]

# criando tempo
time = datetime.strptime('1/1/2000 00:00:00','%m/%d/%Y %H:%M:%S')
dateTime = [time + _*timedelta(minutes = 10) for _ in range(lengthData)]

# criando dados escalares
varEscalares = ['heading', 'pitch', 'roll', 'temp', 'press']

# limites de cada variável

limites = {
    'heading': [180.0, 185.0],
    'pitch': [0, 5],
    'roll': [0, 5],
    'temp': 22,
    'press': 20
    }

# criando célula para conter as variáveis
cell = {}
for var in varEscalares:
    if var == 'press':
        filtro = [math.sin(_)/6 for _ in np.linspace(0,30,lengthData)]
        senoide = [math.sin(_) for _ in np.linspace(0,180,lengthData)]
        for index in range(len(senoide)):
            senoide[index] += filtro[index]*senoide[index]

        cell[var] = [_ + limites['press'] for _ in senoide]
        
    elif var == 'temp':
        var = 'temp'
        filtro = [math.sin(_) for _ in np.linspace(0,30,lengthData)]
        senoide = [math.sin(_) for _ in np.linspace(0,45,lengthData)]
        
        for index in range(len(senoide)):
            senoide[index] += filtro[index]*senoide[index]
            
        temp = [limites[var] + s for s in senoide]
        cell[var] = temp
    else:
        cell[var] = [round(random.uniform(limites[var][0],limites[var][1]),3)\
                     for _ in range(lengthData)]

plt.plot([math.sin(_) for _ in values])

# a = [math.sin(_) for _ in values]
# b = [_/6 for _ in a]

# plt.plot(filtro)
# plt.plot(senoide)
# plt.grid()

# plt.plot(temp)
