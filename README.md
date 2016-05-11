# FinanceML
## Predicting near-term S&P 500 index trends using machine learning
> *This is an open-ended final project for [Dr. Daniel Fabbri](mailto:daniel.fabbri@vanderbilt.edu)'s BigData course at Vanderbilt University.*

## Authors

Ellis Brown
: <ellis.l.brown@vanderbilt.edu> --  [@ellisbrown](https://github.com/ellisbrown)

Danny Carr
: <daniel.p.carr@vanderbilt.edu> --  [@dcarr45](https://github.com/dcarr45)

Max Puidak
: <max.w.puidak@vanderbilt.edu> --  [@maxpudi](https://github.com/maxpudi)



## Introduction

Intelligent stock price prediction in the near-term has nearly unlimited potential. However, designing a model that does so accurately would defy years of academic study and several cornerstones in finance theory. The efficient-market hypothesis (EMH) states that asset prices fully reflect all available information. Under strict EMH, no security in a financial market will ever be mis-priced. Similarly, the random-walk hypothesis states that stock prices follow a random walk in the short-term, and are therefore, unpredictable. Yet, the evolution of machine learning techniques and the availability of ‘big’ data has led critics, scholars, and investors to question the integrity of these theories. It is the goal of this project to use machine learning techniques for the prediction of S&P 500 price trends in the near term (30-days). Specifically, the model attempts to predict the binary classification problem of “will the S&P 500 price rise in 30 days?” Three data sources were used to address our problem: technical indicators, fundamental analysis, and sentiment analysis.

See each subdirectory for its respective description:

1. [Technical Analysis](https://github.com/dcarr45/FinanceML/tree/master/technical)
2. [Fundamental Analysis](https://github.com/dcarr45/FinanceML/tree/master/13F)
3. [Sentiment Analysis](https://github.com/dcarr45/FinanceML/tree/master/SentimentAnalysis)

## Conclusion
With the Technical and Sentiment analyses both yielding workable results, an aggregate features table was able to be created combining the two. In order to maximize the number of rows, each month’s sentiment data fields were duplicated for each day of technical data and appended to the technical feature matrix. When running the combined feature matrix, an AUC of 0.51 was achieved--which, though above 0.5, is a very poor score.

### Conclusions
Almost all of our analyses led to AUC’s right around 0.5, which could imply that we have poorly established our features and labels. If that is not the case, then it implies that there is very low correlation to the data we looked at and whether or not there will be an increase in price of the S&P 500 30 days in the future.

### Future Work
We hope to continue working on this project to devise the best features to include and get a reasonable AUC. We would also like to clean up the code and make the repository more standalone.
