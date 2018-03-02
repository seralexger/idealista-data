# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################

import os.path
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from scipy import spatial

class RentCalc:

	""" Class to make simple calculations with data """

	housing_data = object

	def __init__(self):

		if os.path.isfile('data/rent_housing_data.csv'):
			self.housing_data = pd.read_csv('data/rent_housing_data.csv', delimiter = ';')
		else:
			print('No existe el archivo en la ruta data/rent_housing_data.csv')

	def calc_distance(self, lat, lng, lat2, lng2):
	    """ Haversine Calculus"""

	    lng, lat, lng2, lat2 = map(radians, [lng, lat, lng2, lat2])

	    dlng = lng2 - lng 
	    dlat = lat2 - lat 
	    a = sin(dlat/2)**2 + cos(lat) * cos(lat2) * sin(dlng/2)**2
	    c = 2 * asin(sqrt(a)) 
	    r = 6371

	    return c * r

	def get_area_homes(self, lat, lng, radius):
		""" Get data of homes inside area with center in lat,lng and radius """


		distances = self.housing_data.apply(lambda house: self.calc_distance(lat, lng, house['latitude'], house['longitude']), axis=1) 
		distances = distances[distances <= radius]
		idx = distances.index.values.tolist()
		area_homes = self.housing_data.iloc[idx]
		mean_price = int(area_homes['price'].mean())
		total_rent_houses = distances.count()
		total_rent_size = area_homes['size'].sum()
		mean_size = int(area_homes['size'].mean())
		pricebyarea = int(area_homes['price'].sum()/area_homes['size'].sum())
		total_rooms = area_homes['rooms'].sum()
		mean_rooms = int(area_homes['rooms'].mean())

		return ('Total rent houses inside area is {}'+
				'\nMean price inside area is {} €'+ 
			  	'\nTotal rent size inside area is {} m^2'+
			  	'\nMean rent size inside area is {} m^2'+
			  	'\nTotal rooms inside area is {}'+
			  	'\nMean rooms inside area is {}'+
			  	'\nPrice by area inside area is {} €/m^2').format(total_rent_houses,
			  										mean_price,
			  										total_rent_size,
			  										mean_size,
			  										total_rooms,
			  										mean_rooms,
			  										pricebyarea)



	def find_property(self, lat, lng, nNear = 30):
		""" Find nearest houses """

		distances = self.housing_data.apply(lambda house: self.calc_distance(lat, lng, house['latitude'], house['longitude']), axis=1)
		idx_near_coor = distances.nsmallest(nNear).index.values.tolist()
		homes_info, vector_arr = zip(*[([self.housing_data.loc[x, "price"],self.housing_data.loc[x, "size"]], 
				   [self.housing_data.loc[x, "size"],
				   self.housing_data.loc[x, "rooms"],
				   self.housing_data.loc[x, "bathrooms"]]) for x in idx_near_coor])

		return homes_info, vector_arr

	def calc_price(self, lat, lng, size, rooms, bathrooms):
		""" Calculate the price of a house in a specific location, based on the nearest houses """
		
		homes_info, nearest = self.find_property(lat,lng)
		tree = spatial.KDTree(nearest)
		similarity_value, similar_homes_idx = tree.query([size, rooms, bathrooms], 10)
		near_prices = [homes_info[x][0] for x in similar_homes_idx]
		near_size = [homes_info[x][1] for x in similar_homes_idx]
		pricebyarea = sum(near_prices)/sum(near_size)
		result_price =  int(pricebyarea*size)

		return result_price