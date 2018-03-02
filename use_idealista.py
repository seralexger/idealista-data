# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################


import csv
#import glob
import json
from tqdm import tqdm
from scraper.idealista import Idealista


'''id_safe = ""
housing = []
for path in glob.glob("data/housing/*"):
	#id_safe += path
	housing += json.loads(open(path).read())
housing_arr = []
print(housing[0]["propertyCode"])
for house in housing:
	try:
		if type(house) != dict:
			housing_arr += house
		else:
			housing_arr.append(house)
	except Exception as e:
		print(e)
		print(house)

id_safe = []
housing_rent = []

for item in housing_arr:
	if item["propertyCode"] not in id_safe:
		id_safe.append(item["propertyCode"])
		housing_rent.append(item)

with open('data/rent_housing_data.json', 'w') as fp:
	json.dump(housing_rent, fp, indent = 4)'''

#Simple way to obtain data on rental houses in Spain, it is possible to use proxies, but I did not see it necessary

scraper = Idealista()
reader = csv.reader(open('data/utils/spain_cities.csv', 'r', encoding = 'latin1'), delimiter=';')
headers = next(reader, None)
spain_cities = list(reader)


for item in tqdm(spain_cities):
	suggest_place = scraper.suggest_places(item[2])
	for location in suggest_place:
		try:
			loc_id = location['locationId']
		except:
			continue
		suggest_location = scraper.suggest_location(loc_id)
		if suggest_location != []:
			search = []
			for loc in suggest_location:
				try:
					loca_id = loc['locationId']
				except:
					continue
				search, total = scraper.search_by_name(loc['name'], loca_id)
				for i in range(2, total):
					search += scraper.search_by_name(loc['name'], loc['locationId'], i)
				if search != []:
					with open('data/housing/'+location['name'].replace("/",",")+'_'+loc['name'].replace("/",",")+'_'+loc['locationId']+'.json', 'w') as fp:
						json.dump(search, fp, indent = 4)