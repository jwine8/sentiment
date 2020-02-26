# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:53:44 2020

@author: admin_guest
"""
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
#cols = ['sentiment','id','date','query_string','user','text']
df = pd.read_csv(r'C:\Users\admin_guest\Documents\mod16.csv')
# above line will be different depending on where you saved your data, and your file name
df.head()
