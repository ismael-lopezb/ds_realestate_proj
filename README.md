# Apartment Price Estimator: Project Overview
* Created a tool that estimates apartment price in Mexico City to help construction companies estimate the potential price of their apartments.
* Scraped over 25,000 apartment descriptions from Inmueble24 using python and BeautifulSoup
* Engineered features from the text of each apartment description to quantify the value of amenities, such as pool, garden, etc.
* Optimized Linear, Ridge, and Gradient Boosting Regressor using GridsearchCV to reach the best model.
## Code and Resources Used
**Python Version:** 3.8.5
**Pckages:** pandas, numpy, sklearn, matplotlib, seaborn, statistics, BeautifulSoup
**Scraper Github:** https://github.com/jorgeviz/depcdmx/tree/master/scrapers
## Web Scraping
Tweaked the web scraper github repo (above) to scrape 25,000 apartment postings from inmueble24.com. With each job, we got the following:
* Name
* Location
* Description 
* Link 
* Price 
* Operation 
* Rooms 
* Bathrooms 
* Construction (m2) 
* Terrain (m2)
## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:
* Replaced the NaN of rooms and baths with the median of the rooms
* Remplaced the NaN of terrain with the corresponding construction and viss
* Removed the rows that have NaN in terrain or contruction 
* Added a column of divisa to convert prices in USD to MXN
* Added the column Delegacion
* Extracted amenities from description column:
  * gym, 
  * pool, 
  * pet fiendly
  * garage
  * Elevator
  * Roof garden
## Exploratory data analysis
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the data.
