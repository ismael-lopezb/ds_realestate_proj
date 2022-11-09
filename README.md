# Apartment Price Estimator: Project Overview
* Created a tool that estimates apartment price in Mexico City to help construction companies estimate the potential price of their apartments.
* Scraped over 25,000 apartment descriptions from Inmueble24 using python and BeautifulSoup
* Engineered features from the text of each apartment description to quantify the value of amenities, such as pool, garden, etc.
* Optimized Linear, Ridge, and Gradient Boosting Regressor using GridsearchCV to reach the best model.
## Code and Resources Used
* **Python Version:** 3.8.5
* **Pckages:** pandas, numpy, sklearn, matplotlib, seaborn, statistics, BeautifulSoup
* **Scraper Github:** https://github.com/jorgeviz/depcdmx/tree/master/scrapers
## Web Scraping
Tweaked the web scraper github repo (above) to scrape 25,000 apartment postings from inmueble24.com. With each apartment, we got the following:
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
  * Gym 
  * Pool 
  * Pet fiendly
  * Garage
  * Elevator
  * Roof garden
## Exploratory data analysis
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the data.

Price distribution: 

<img src="https://github.com/ismael-lopezb/ds_realestate_proj/blob/master/distri.png" alt="Price Distribution" width="500" height="500"/> 

Correlation matrix:

<img src="https://github.com/ismael-lopezb/ds_realestate_proj/blob/master/heatmap.jpg" alt="Correlation matrix" width="500" height="500"/>

Median Price by Delegacion: 
|             Delegacion | Price (MP) |
|-----------------------:|:----------:|
|         Miguel Hidalgo |  14.000000 |
|  Cuajimalpa de Morelos |  12.900000 |
| La Magdalena Contreras |   6.000000 |
|         Alvaro Obregón |   5.750000 |
|             Cuauhtémoc |   5.149000 |
|                Tlalpan |   4.400000 |
|          Benito Juárez |   4.350000 |
|               Coyoacán |   3.090000 |
|           Azcapotzalco |   1.800000 |
|      Gustavo A. Madero |   1.690000 |
|              Iztacalco |   1.380000 |
|    Venustiano Carranza |   1.215000 |
|             Iztapalapa |   0.610000 |
|                Tláhuac |   0.520460 |
|             Xochimilco |   0.413149 |

<img src="https://github.com/ismael-lopezb/ds_realestate_proj/blob/master/pricepd.png" alt="Price by Delegacion" width="500" height="500"/>

The more expensive Colonias:

<img src="https://github.com/ismael-lopezb/ds_realestate_proj/blob/master/pricebcnl.png" alt="Price nlargest" width="500" height="500"/>

The cheapest Colonias: 

<img src="https://github.com/ismael-lopezb/ds_realestate_proj/blob/master/pricebcns.png" alt="Price nsmallest" width="500" height="500"/>

## Model Building
First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%
I tried four different models and evaluated them using Root Mean Squared Error. 
I tried four different models:
* **Multiple Linear Regression** – Baseline for the model
* **Ridge Regression** - Because of the sparse data from the many categorical variables
* **Lasso Regression** - An alternative to Ridge Regression
* **Gradient Boosting Regressor** - Again, with the sparsity associated with the data, I thought that this would be a good fit.
## Model performance
The Gradient Boosting Regressor model far outperformed the other approaches on the test and validation sets.
* **Gradient Boosting Regressor:** RMSE = 0.4545
* **Ridge Regression:** RMSE = 0.5418
* **Multiple Linear Regression:** RMSE = 0.5419
* **Lasso Regression:** was discarded because it had a MSE=0.999
