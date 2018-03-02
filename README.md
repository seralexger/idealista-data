# idealista-data
 
I built an unofficial class to use some idealistic characteristics. Then I use it to obtain data on rental housing in Spain, in order to play a bit with this data, and I built a simple prediction class of the value of the rental house.

## Getting Started

All the necesary libraries for run the project are in the requirements.txt.

### Use of the class

There is a simple practical example in idealista_get_data_simple.py, you can use proxies and parallelize but I did not see it necessary.

```
from scraper.idealista import Idealista

idea_scraper = Idealista()

idea_scraper.suggest_places(prefix = 'ma', credentials = None, proxy = None)
idea_scraper.suggest_location(location_id = '0-EU-ES-28-07-001-079', credentials = None, proxy = None)
idea_scraper.search_by_name(place_name = 'Madrid', place_id = '0-EU-ES-28-07-001-079', nPage = 1, credentials = None, proxy = None)
idea_scraper.search_by_area(lat, lng, distance, nPage = 1, credentials = None, proxy = None)
```

## Analyze the data

With all the idealista rental data of Spain, we can made some graphs to have a quick view of the information, for make this represantation and other simple representations you can find code in plot_sample.py.

### Rental density

```
#Density rent homes
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.05)
plt.show()
```

![alt text](https://raw.githubusercontent.com/seralexger/idealista-data/master/data/images/rental_density_readme.png)

### Price gradient

```
#Color gradient home prices
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.3, 
				  c='price', cmap=plt.get_cmap('jet'), colorbar=True, vmin=0, vmax= 1000)
plt.show()
```

![alt text](https://raw.githubusercontent.com/seralexger/idealista-data/master/data/images/price_gradient_readme.png)

## RentCalc

It is a class to do some calculations, you can get information about an area based on latitude, longitude and a radius in km, and you can calculate the rental price of a house based on your nearest similar houses.

```
from rentCalc import RentCalc

CALC = RentCalc()

predicted_price = CALC.calc_price(lat, lng, size, rooms, bathrooms)

#radius in km
print(get_area_homes(lat, lng, radius))

```

In start_rentCalc.py there is a simple CLI interface for use this class, this is an example:

![alt text](https://raw.githubusercontent.com/seralexger/idealista-data/master/data/images/rentCalc_readme.png)


