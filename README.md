# idealista-data
 I have built an unofficial class to use some characteristics of idealista. Then I use it to get rent housing data from Spain, with the purpose of play a little with this data, and built a simple prediction model of house value.

## Getting Started

All the necesary libraries for run the project are in the requirements.txt.

### Use of the class

There is a practical example in use_example.py

```
from scraper.idealista import Idealista

idea_scraper = Idealista()

idea_scraper.suggest_places(prefix, credentials = None, proxy = None)
idea_scraper.suggest_location(location_id, credentials = None, proxy = None)
idea_scraper.search_by_name(place_name = 'Madrid', place_id = '0-EU-ES-28-07-001-079', nPage = 1, credentials = None, proxy = None)
idea_scraper.search_by_area(lat, lng, distance, nPage = 1, credentials = None, proxy = None)
```

## Analyze the data

With all the idealista rent data of Spain, I have made some graphs to have a quick view of the information.

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
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.3, c='price', cmap=plt.get_cmap('jet'), colorbar=True, vmin=0, vmax= 1000)
plt.show()
```

![alt text](https://raw.githubusercontent.com/seralexger/idealista-data/master/data/images/price_gradient_readme.png)