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

lengthData = 4466 # tamanho do dado a ser criado: equivale a 30 dias de 10 em 10 min

time = datetime.strptime('1/1/2000 00:00:00','%m/%d/%Y %H:%M:%S')
dateTime = [time + _*timedelta(minutes = 10) for _ in range(lengthData)]
dateTime[-1]
