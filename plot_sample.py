# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix



housing_data = pd.read_csv('data/rent_housing_data.csv', delimiter = ';')

#Density rent homes
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.05)
#plt.savefig('data/images/density_map.png', dpi=720)

#Color gradient home prices
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.3, c='price', cmap=plt.get_cmap('jet'), colorbar=True, vmin=0, vmax= 1000)
#plt.savefig('data/images/price_map.png', dpi=720)

#housing_data.hist(bins=50, figsize=(20,10))
attr = ['price', 'rooms', 'size', 'latitude', 'longitude']
corr_matrix = housing_data.corr()
print(corr_matrix['bathrooms'].sort_values(ascending = False))
#scatter_matrix(housing_data[attr], figsize=(12,10), vmin=0, vmax= 1000)

#plt.scatter(housing_data['bathrooms'], housing_data['price'])
#plt.ylim(-5, -3)
#plt.xlim(40, 41)

#housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.05)
#housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4, s=housing_data['size']/100, label='size',c='price', cmap=plt.get_cmap('jet'), colorbar=True, vmin=0, vmax= 1000)
#housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.3, c='price', cmap=plt.get_cmap('jet'), colorbar=True, vmin=0, vmax= 1000)
#plt.legend()
#housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.1, s=housing_data['size']/100, label='size')
plt.show()