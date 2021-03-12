## Scheduler module that schedule following services:

- News Scraping services that fetch news from specialized financial newsgroupes and POST data to our Mongo engine Services.
- Data providing services including Market information (from [finnhub API](https://finnhub.io/)) and news from our Mongo engine services. 
- Model training services that fetch data from our data providing services and work on Tensorflow 2. 
- Prediction Services that predict particular currency pairs and work on Tensorflow2.



### News Scraping Service

This service automaticaly connected to the specialized financial news groupes every 60 minutes with scaduler module and scrap the latest news. Then store all scraped news into MongoDB dataset.
#### Currenly available resources are:

 -  [FXStreet](https://www.fxstreet.com/news) for Forex currency pairs news scraping
 - [FXStreet Cryptocurrency Section](https://www.fxstreet.com/cryptocurrencies/news) for cryptocurrencies news scraping
 - [NewsBTC](https://www.newsbtc.com/) for cryptocurrencies news scraping
 - [cointelegraph](https://cointelegraph.com/) for cryptocurrencies news scraping
 - [Investing](https://www.investing.com/) for commodities news scraping (Gold, Metals, Oil, Gas)
 - [Google News API]() for scraping the latest news from specialized newsgroups such as Reuters or Bloomberg. I did scraping of all news about Forex and cryptocurrencies market.
 

For checking our news Scraping Services, please refer to newsScraper folder

<hr/>

### Data providing services
For checking our news data providing services, please refer to dataProvidingServices folder.

<hr/>

### Model training services
This services currently available for four currency pairs of [ EUR_USD , USD_JPY , GBP_USD , BTC_USDT] based on resolution 60 minutes.
With these services we schedule our predictive model training every business day. The implementation of our predictive model is based on **BERT based BoEC** text representation and Recurrent Convolution neural network which implemented in **KERAS functional API**.
We train our predictive modeles based on **over 2 years** of our news data .
For checking our news data providing services, please refer to TrainingServices folder.

<hr/>

### Prediction services
This services currently available for two categories of Forex and cryptocurrency markets and also four currency pairs of [ EUR_USD , USD_JPY , GBP_USD , BTC_USDT] based on resolution 60 minutes.
We schedule our prediction services every in business days and POST the predicted values to our Mongo engine services.
For checking our news data providing services, please refer to predictionServices folder.