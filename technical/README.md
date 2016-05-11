# Technical Indicator
> *Max Puidak*

In our technical indicator approach, daily price change, 30-day historical volatility, and relative strength index (RSI) were used as features for an ETF that tracks the S&P 500 and the top ten S&P 500 components by weight. Data was compiled from Jan 1st, 2000 to Mar 30th, 2016, with each day representing a row. The final feature matrix was [4017 x 33] [rows x feature], The number of rows is equivalent to the number of trading days in the previously mentioned time period. There are 3 features per stock, and 11 total stocks (3*11 = 33).


## Data Collection

|Company Name|Ticker|
|---|---|
|SPDR S&P 500 ETF Trust|SPY|
|Apple Inc.|AAPL|
|Microsoft Corp.|MSFT|
|Exxon Mobil Corp.|XOM|
|Johnson & Johnson|JNJ|
|General Electric Co.|GE|
|Berkshire Hathaway Inc. Class B|BRK.B|
|Amazon.com Inc.|AMZN|
|Wells Fargo & Co.|WFC|
|JPMorgan Chase & Co.|JPM|
|AT&T Inc.|T|

Stock price data was obtained from Yahoo! Finance using the pandas remote data access library. Historical data [Date, Open, High, Low, Close, Volume, Adjusted Close] for the top ten S&P 500 components by weight was imported to a pandas data frame and written to a CSV-file.  Facebook (FB) Inc.’s initial public offering took place on May 18, 2012. Data was pulled from January 1st, 2000 to March 30th 2016; therefore, FB was replaced by the 11th largest component, AT&T (T) in our data analysis. The end date was chosen because at the time of this project’s start, March 30th was 31 trading days prior, which is equal to the time buffer required for data labeling. Additionally, the SPDR S&P 500 ETF (SPY) was used as a benchmark to track the S&P 500. The final stocks used for feature construction are listed in Table 1. The list of tickers was stored in a CSV file and is loaded at the beginning of the getData.py program. All of the technical indicators used in our final feature matrix can be calculated solely using the adjusted closing price (Adj. Close) for each ticker. Date, which was used as an index to keep track of the time series, and Adj. Close were sliced from the raw CSV-files and passed to the relevant transformation algorithms. Adjusted closing price is a better metric for examining historical returns than simple closing price because it accounts for any distributions and corporate actions that occurred at any time prior to the next day’s open such as Apple Inc.’s June 2014 7:1 stock split.

## Data Transformation

This program was designed so that data would be retrieved, processed, and transformed for each ticker sequentially, then aggregated in the final feature matrix. Each transformation algorithm is passed one parameter, the company's stock ticker. This approach was chosen with feature optimization and scalability in mind. Adding, removing, and changing stock list constituents only requires altering the original tickers.csv file. Additionally, technical indicators can be added/removed to the feature list as needed. Three technical indicators were used for each ticker: daily return, 30-day historical volatility, and relative strength index (RSI). Equations for each indicator are listed below. Each indicator transformation requires the adjusted closing price time series. Daily return represents the percent change in adjusted closing price from the previous to current day. Historic volatility is a representation of variance in the stock price in the prior 30 days. RSI is a momentum indicator that compares the magnitude of recent gains to recent losses to determine overbought and oversold conditions. An RSI of 50 indicates the price of a stock is at the same level as 14 days prior. As RSI approaches 70, the stock is believed to have been overbought and is getting overvalued. As RSI approaches 30, it is considered to be oversold and undervalued.

The integrity of the time series for each ticker is preserved in the date/indicator pairs until the final join during feature matrix construction. For example, 30-day volatility requires the previous 30 days’ data, RSI requires the previous 14 days’, and our label is based on the current price and the price in 30 days. Each transformation maintained the original [2 x 4077] Adj. Close numpy-array shape. Following the final join of all features, the first and last 30 rows of data were trimmed from the feature matrix to account for the missing values.

![equations](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Equations")


## Feature Construction and Data Labeling

The final feature matrix was constructed by joining the pandas dataframes containing daily return, 30-day volatility, and RSI, indexed by date. The first and last 30 rows of data were removed from the matrix to account for the missing indicators based on a rolling time window. The final feature matrix contained 4017 rows (the number of trading days in since January 1st, 2000) and 33 features (3 technical indicators per S&P 500 component, plus the SPY ETF). Binary classification was used to label the data. If the price of SPY on a given day was less than the the price in 30 days, the output was a 1, indicating the S&P was in the midst of an uptrend. If the price declined, the output was a 0, indicating a downtrend.


## Model Fitting and Classification
The scikit-learn library was used for a binary classification model. Random forest and linear support vector machine classifiers were used. Our baseline was the daily return of SPY. The data was trained and tested using the StratifiedKFold() scikit learn function to separate the data. Two-fold train/testing was the only combination that yielded an AUC of over 0.5. Results of the different models are listed below.

|Classifier|Mean AUC|
|---|---|
|Random Forest Baseline|0.493766456|
|Random Forest Model|0.476769257|
|Linear SVM Baseline|0.492715145|
|Linear SVM Model|0.508899004|

## Results and Discussion

Our model beat our baseline and the AUC of our model is above 0.5. However, in order to use the model to profit from the market, a vastly higher confidence level is required. It is believed that upon feature optimization (removing overweighting and features that can cause over-fitting), the model could be greatly improved. It is also believed that including more relevant features such as securities from other world markets, other indicators found on company quarterly 10K-forms could also improve the model. Additionally, including different rolling windows for the features could prove useful. Future work will include improved feature generation and optimization. Ideally, this model could be used to profit off the market.
