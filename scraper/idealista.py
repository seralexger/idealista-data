# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################

import requests
import json
import random
import string
import os.path
import time
import math
import hashlib


class Idealista:
	"""
	Idealista v 1.0

	This is an unofficial class for use some of idealista features.

	Filter types:

			operation:	sale
					  	rent

			propertyType:	bedrooms
							building
							buildings
							chalet
							countryhouse
							flat
							garage
							garages
							homes
							house
							land
							lands
							newDevelopment
							newDevelopments
							office
							offices
							premise
							premises
							room
							storageRoom
							storageRooms
							storageroom

			order:	weight
					publicationDate
					price
					priceDown
					ratioeurm2
					size
					floor

			sort:	desc
				 	asc

	"""
	credentials = {}
	base_headers = {}

	auth_url = 'https://secure.idealista.com/api/oauth/token'
	creation_url = 'https://secure.idealista.com/api/3/es/user/create'
	
	base_filter = {'order': 'weigh', 
				   'mPolygons': '[com.idealista.android.domain.model.polygon.Polygon@0]', 
				   'propertyType': 'homes',
				   'locale': 'es',
				   'maxItems': '50',
				   'numPage': '1',
				   'operation': 'rent',
				   'distance': '0',
				   'sort': 'desc',
				   'gallery': 'true',
				   'quality': 'high'
				   }

	def __init__(self):
		""" Init credentials or generate new credentials if doesn't exist """

		if os.path.isfile('scraper/user_credentials.json'):
			self.credentials = json.loads(open('scraper/user_credentials.json').read())
			self.credentials['access_token'] = self.generate_auth()
		else:
			self.credentials = self.generate_credentials()
			with open('scraper/user_credentials.json', 'w') as fp:
				json.dump(self.credentials, fp, indent = 4)

		self.base_headers['Authorization'] = 'Bearer ' + self.credentials['access_token']

	def get_polygon(self, lat, lng, distance):
		""" Calculate circle coordenates for search area """

		R = 6378.1
		num_points = 65
		polygon = []

		for index in range(num_points):

			dgr_space = math.degrees((360/num_points) * index) 

			lat_base = math.radians(lat) 
			lon_base = math.radians(lng) 

			calc_lat = math.asin( math.sin(lat_base)*math.cos(distance/R) +
			     math.cos(lat_base)*math.sin(distance/R)*math.cos(dgr_space))

			calc_lon = lon_base + math.atan2(math.sin(dgr_space)*math.sin(distance/R) * math.cos(lat_base),
			             math.cos(distance/R)-math.sin(lat_base)*math.sin(calc_lat))

			calc_lat = math.degrees(calc_lat)
			calc_lon = math.degrees(calc_lon)
			polygon.append([calc_lon, calc_lat, 0])

		polygon[len(polygon)-1] = polygon[0]
		return [[polygon]]

	def random_string(self, mode, lngRan):

		if mode == 0:
			chars = string.ascii_lowercase + string.digits
			return ''.join(random.choice(chars) for x in range(lngRan))
		elif mode == 1:
			chars = string.digits
			return ''.join(random.choice(chars) for x in range(lngRan))
		else:
			chars = string.ascii_lowercase
			return ''.join(random.choice(chars) for x in range(lngRan))

	def modify_filter(self,
					  order = 'weigh', 
					  mPolygon = '[com.idealista.android.domain.model.polygon.Polygon@0]', 
					  propertyType = 'homes', 
					  locale = 'es', 
					  maxItems = '50',
					  numPage = '1', 
					  operation = 'rent', 
					  distance = '0',  
					  sort = 'desc', 
					  gallery = 'true', 
					  quality = 'high',):
		""" Modify the base filter """

		self.base_filter['order'] = order
		self.base_filter['mPolygons'] = mPolygons
		self.base_filter['propertyType'] = propertyType
		self.base_filter['locale'] = locale
		self.base_filter['maxItems'] = maxItems
		self.base_filter['numPage'] = numPage
		self.base_filter['operation'] = operation
		self.base_filter['distance'] = distance
		self.base_filter['sort'] = sort
		self.base_filter['gallery'] = gallery
		self.base_filter['quality'] = quality
			

	def generate_auth(self, proxy = None):
		""" Generate access token """
		auth_headers = {
						'Accept': 'application/json, text/html',
						'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
						'Authorization': 'Basic NWI4NWMwM2MxNmJiYjg1ZDk2ZTIzMmIxMTJlZTg1ZGM6aWRlYSUzQmFuZHIwMWQ=',
						'Host': 'secure.idealista.com',
						}

		data = 'grant_type=client_credentials&scope=write'
		response = requests.post(self.auth_url, headers = auth_headers, data = data, proxies = proxy)
		res_json = json.loads(response.content)

		return res_json['access_token']


	def generate_credentials(self, proxy = None):
		""" Generate new credentials """

		access_token = self.generate_auth(proxy)
		k_object = self.random_string(0, 32)
		t_object = self.random_string(1,14) + "." + self.random_string(1,16)
		email = self.random_string(3, 9) + '@gmail.com'
		password = self.random_string(0, 7)
		username = self.random_string(3, 7)
		timestamp = str(int(time.time()*1000))

		user_headers = {
					'Accept': 'application/json, text/html',
					'Authorization': 'Bearer ' + access_token,
					'app_version': '7.8.5',
					'Host': 'secure.idealista.com',
					}

		data = [
				  ('k', k_object),
				  ('t', t_object),
				  ('email', email),
				  ('password', password),
				  ('alias', username),
				]

		response = requests.post(self.creation_url, headers = user_headers, data = data, proxies = proxy)
		res_json = json.loads(response.content)

		credentials_dic = {'access_token': access_token, 
						   'server_token': res_json['token'],
						   'token': (hashlib.md5(bytes(res_json['token']+timestamp,"ascii"))).hexdigest(),
						   'api_key': res_json['apikey'],
						   'timestamp': timestamp,
						   'k_object': k_object,
						   't_object': t_object,
						   'email': email,
						   'username': username,
						   'password': password}

		return credentials_dic


	def suggest_places(self, prefix = 'ma', credentials = None, proxy = None):
		""" Suggestions for sites given a prefix """

		suggest_headers = {
		    'Authorization': 'Bearer ' + self.credentials['access_token'],
		}
		#print(prefix)
		params = (
		    ('user', self.credentials['email']),
		    ('token', self.credentials['token']),
		    ('timestamp',  self.credentials['timestamp']),
		    ('prefix', prefix),
		    ('showPois', 'true'),
		    ('t', self.credentials['t_object']),
		    ('k', self.credentials['k_object']),
		)

		response = requests.get('https://secure.idealista.com/api/3/es/locations', headers= self.base_headers, params=params, proxies = proxy)
		res_json = json.loads(response.content)
		#print(res_json)
		return res_json['locations']

	def suggest_location(self, location_id = '0-EU-ES-28-07-001-079', credentials = None, proxy = None):
		""" Suggestions for location given a suggested place id """
		
		params = (
		    ('user', self.credentials['email']),
		    ('token', self.credentials['token']),
		    ('timestamp', self.credentials['timestamp']),
		    ('locationId', location_id),
		    ('showPois', 'true'),
		    ('t', self.credentials['t_object']),
		    ('k', self.credentials['k_object']),
		)

		response = requests.get('https://secure.idealista.com/api/3/es/locations', headers= self.base_headers, params=params, proxies = proxy)
		res_json = json.loads(response.content)

		return res_json['locations']

	def search_by_name(self, place_name = 'Madrid', place_id = '0-EU-ES-28-07-001-079', nPage = 1, credentials = None, proxy = None):
		""" Search by place name and place id """
		
		params = (
				    ('numPage', str(nPage)),
				    ('t', self.credentials['t_object']),
				    ('k', self.credentials['k_object']),
				    ('user', self.credentials['email']),
				    ('token', self.credentials['token']),
				    ('timestamp', self.credentials['timestamp']),
				    ('order', self.base_filter['order']),
				    ('propertyType', self.base_filter['propertyType']),
				    ('locale', self.base_filter['locale']),
				    ('maxItems', self.base_filter['maxItems']),
				    ('locationName', place_name),
				    ('operation', self.base_filter['operation']),
				    ('locationId', place_id),
				    ('distance', self.base_filter['distance']),
				    ('sort', self.base_filter['sort']),
				    ('gallery', self.base_filter['gallery']),
				    ('quality', self.base_filter['quality']),
				)


		response = requests.post('https://secure.idealista.com/api/3.5/es/search', headers=self.base_headers, params=params, proxies = proxy)
		res_json = json.loads(response.content)
		
		return res_json['elementList'], res_json['totalPages']

	def search_by_area(self, lat, lng, distance, nPage = 1, credentials = None, proxy = None):
		""" Search by coordenates and distance """

		polygon = self.get_polygon(lat, lng, distance)


		params = (
					('numPage', str(nPage)),
				    ('t', self.credentials['t_object']),
				    ('k', self.credentials['k_object']),
				)

		data = (
				('user', self.credentials['email']),
				('token', self.credentials['token']),
				('timestamp', self.credentials['timestamp']),
				('shape', '{"type":"MultiPolygon","coordinates":'+str(polygon)+'}'),
				('order', self.base_filter['order']),
				('mPolygons', self.base_filter['mPolygons']),
				('propertyType', self.base_filter['propertyType']),
				('locale', self.base_filter['locale']),
				('maxItems', self.base_filter['maxItems']),
				('locationName', 'Tu+zona+personalizada'),
				('numPage', self.base_filter['numPage']),
				('operation', self.base_filter['operation']),
				('distance', self.base_filter['distance']),
				('sort', self.base_filter['sort']),
				('gallery', self.base_filter['gallery']),
				('quality', self.base_filter['quality']),
			)

		response = requests.post('https://secure.idealista.com/api/3.5/es/search', headers = self.base_headers, params=params, data = data, proxies = proxy)

		res_json = json.loads(response.content)

		return res_json['elementList'], res_json['totalPages']
