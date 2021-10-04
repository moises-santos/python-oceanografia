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
import scipy.stats as stats

lengthData = 4465 # tamanho do dado a ser criado: equivale a 30 dias de 10 em 10 min
quantSpike = 150 # quantidades de spikes

indexSpike = [random.randint(0, lengthData) for _ in range(quantSpike)]

# criando tempo
time = datetime.strptime('1/1/2000 00:00:00','%m/%d/%Y %H:%M:%S')
dateTime = [time + _*timedelta(minutes = 10) for _ in range(lengthData)]

#%% criando dados escalares
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
        data = [round(random.uniform(limites[var][0],limites[var][1]),3)\
                     for _ in range(lengthData)]
        roundData = gaussian_filter1d(data, sigma = 10) 
        cell[var] = roundData
        
# verificando visualmente os dados
for var in varEscalares:
    plt.figure()
    plt.plot(cell[var], label = var)
    plt.title('max %s %.2f'%(var, max(cell[var])))

# criando spikes
dfout = {}
# exportando variáveis criadas
for var in varEscalares:
    dfout[var] = pd.DataFrame(cell[var],dateTime)
    dfout[var].to_csv('%s.csv'%var, header = None, float_format = '%.3f')

#%% criando dados matriciais

varMatricial = ['vel', 'dir', 'amp', 'cor']

celulasTotais = int(max(cell['press'])) + 1

fatorVel = np.linspace(.25, 1, celulasTotais)
sigma = math.sqrt(0.15)
x = np.linspace(0 - sigma, 0 + sigma, celulasTotais)
fatorAmp = stats.norm.pdf(x, 0, sigma)*90
min(fatorAmp)
max(fatorAmp)

shape = [len(dateTime), celulasTotais]
cellMatriz = {}

# criando matriz "vazia"
array = np.empty(shape)

limites = {'vel':[1,2],
           'dir':[[30,120],[210,300],[120,210]],
           'amp':[max(fatorAmp), 100],
           'cor':[max(fatorAmp)*2, max(fatorAmp)*2.5]
           }

# criando array de dados dentro das celulas
for var in varMatricial:
    cellMatriz[var] = np.copy(array)
    if var == 'vel':
        for row in range(len(array)):
            cellMatriz[var][row,:] = [random.uniform(limites[var][0],limites[var][1])\
                                      for _ in range(celulasTotais)]
            for col in range(celulasTotais):
                cellMatriz[var][row,col] = fatorVel[col]*cellMatriz[var][row,col]
            cellMatriz[var][row,round(cell['press'][row])] =\
                cellMatriz[var][row,round(cell['press'][row])]*1.25
    # # verificação visual do campo de velocidade
    # plt.imshow(cellMatriz['vel'].T,
    #            aspect='auto',
    #            interpolation = 'nearest',
    #            origin = 'lower',
    #            cmap='jet')
    
    elif var == 'dir': # levar em consideração a maré para alternancia da direção
        for row in range(len(array)):
            cellMatriz[var][row,:] = [random.uniform(limites[var][0],limites[var][1])\
                                      for _ in range(celulasTotais)]
                
            
    elif var == 'amp':
        for row in range(len(array)):
            cellMatriz[var][row,:] = [random.uniform(limites[var],limites[var])\
                                      for _ in range(celulasTotais)]
    else:
        for row in range(len(array)):
            cellMatriz[var][row,:] = [random.uniform(limites[var],limites[var])\
                                      for _ in range(celulasTotais)]
        