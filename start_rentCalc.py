# -*- coding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/idealista-data
#
#########################################################

from rentCalc import RentCalc


def ask_data(CALC):
    ''' Ask  for data '''

    print("Introduce los datos:")
    print("Mode: \n0 - Calcula precio de casa\n1 - Obten información en un area")
    while True:
        letter = input()

        if letter == "0":
            print("\033[H\033[J")
            print('Introduce los datos separados por comas: lat,lng,size,rooms,bathrooms')
            data = input().split(",")
            print('{}€'.format(CALC.calc_price(float(data[0]),float(data[1]),int(data[2]),int(data[3]),int(data[4]))))
            return
        else:
            print("\033[H\033[J")
            print('Introduce los datos separados por comas: lat,lng,radius')
            data = input().split(",")
            print(CALC.get_area_homes(float(data[0]),float(data[1]),int(data[2])))
            return

if __name__ == "__main__":

    CALC = RentCalc()

    while True:
        ask_data(CALC)
