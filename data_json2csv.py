# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################

import csv
import glob
import json
from tqdm import tqdm

csv_headers = ['propertyCode', 'firstActivationDate','floor', 'price', 'propertyType', 'size', 'exterior', 'rooms', 'bathrooms', 'province', 'municipality','latitude', 'longitude', 'newDevelopment','hasLift', 'hasParkingSpace', 'isParkingSpaceIncludedInPrice', 'priceByArea', 'district']
housing = json.loads(open('data/rent_housing_data.json').read())
csv_doc = []

for house in tqdm(housing):
	csv_data = []
	for header in csv_headers:
		if header not in house:
			if header == 'district':
				csv_data.append(house['municipality'])
			elif header == 'hasParkingSpace' or header == 'isParkingSpaceIncludedInPrice':
				if 'parkingSpace' in house:
					csv_data.append(house['parkingSpace'][header])
				else:
					csv_data.append(False)
			else:
				csv_data.append(None)
		else:
			csv_data.append(house[header])
	csv_doc.append(csv_data)

with open('data/rent_housing_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter = ';')
    writer.writerow(csv_headers)
    writer.writerows(csv_doc)