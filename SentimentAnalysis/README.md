# Sentiment Analysis
> *Ellis Brown*

It is well known that news items can bear significant impact on the prices and holdings of a stock. Good news about the
company, or even mention of the company in a positive article can give a boost to the company in the eyes of the
consumer who is buying or selling shares of the company; likewise, bad news or mention in a negative context can result
in a negative impact on the company.  With the rise of the internet, the amount of information on all companies has
boomed. Consumers have turned more and more towards the growing number of online sources to get their news, and thus
have many more opportunities to see positive or negative sentiments about a company. For this reason, performing a
sentiment analysis on a company is likely to give a good indication on the future performance of the company’s stock.

There are many ways of approaching a sentiment analysis. Due to the need to examine the sentiment of a company at a
specific time and predict the future performance of the stock, sets of articles published in a given month involving a
specific company were studied for number of positive and number of negative references in order to yield a number of
sentiment indicators for the company in the given month.
    
    By analyzing the monthly historical sentiment data for each of the top ten performers in the S&P 500, we hope to be
    able to predict if the price of the S&P 500 itself (or SPY, which mirrors the S&P) will increase by the next month.

    ##  Data Collection
    Sentiment data proved to be more difficult to obtain than expected. The initial attempt at an approach was to use
    Google News, as it is an aggregator of news sources throughout the web. The API has been depreciated for a number of
    years, so I turned to manually altering news.google.com/archivesearch urls with a company name, start date, and end
    date. I then would pull the resulting html, parse it using Beautifulsoup, and perform my sentiment search on the
    words in the results. After running a good number of searches in this way, google caught on that my searches were
    coming from a script and not a manual search and began rerouting each of my queries to a CAPTCHA page -- thus
    nullifying any of the progress that I had made.

    After testing numerous other news search APIs, I settled upon The New York Times API to fuel my data collection. I
    performed searches on each of the companies we are examining along with its ticker name for each month in our
    daterange. I dumped the json result from each search to a file in order to prevent having to query NYT’s server
    again if I changed the sentiment analysis. I performed the sentiment analysis on the lead paragraph, headline,
    abstract, snippet, and keywords that were returned from the search.

    In order to count the number of positive and negative references, I downloaded a pre-existing dictionary of words
    with corresponding sentiments, and took the positive and the negative slices of the dictionary. When scanning
    through words pulled from a search result, I would check each word against my positive and negative dictionaries,
    keeping track of number of positive terms encountered (p), number of negative terms encountered (n), and total
    number of terms encountered (N). 

    ## Data Transformation
    For each date and for each company, I used n, p, and N to calculate 5 sentiment indicators: polarity, subjectivity,
    positive references per reference, negative references per reference, and sentiment differences per reference. These
    sentiment indicators are all centered around 0, which is one desire of data preprocessing. I stored this data to a
    .csv file, with each row representing one month and each column representing one of the sentiment indicators for one
    of our companies.


    ## Feature Construction and Data Labeling
    The final feature matrix is each sentiment indicator for each company for each month in our range, resulting in 190
    rows (months) and 60 columns (features).
    In order to make my label matrix -- with a 1 at the month’s entry if the adjusted close price at the end of the
    month was greater than the adjusted close price at the open of the month -- I created a matrix with SPY’s daily
    adjusted close and then examined the adjusted close at the first trading day of the month vs the last trading day of
    the month. As previously mentioned, this is an example of a binary classifier.

    ## Model Fitting and Classification
    In order to determine the best baseline and best classifiers, I wrote a large script that tested each of my
    individual features under a number of classifiers. The initial set of classifiers was Stochastic Gradient Descent
    (SGD), Gaussian Naïve Bayes, Random Forest, and Linear Support Vector Machine (SVM).  For each of my features, I ran
    each of these classifiers on a baseline matrix (190 rows, 1 column) and wrote the AUC to a .csv file. I loaded the
    .csv into Excel and manipulated the data to find the average, standard deviation, and variance of the result data in
    search of which feature had an AUC closest to 0.5 the most frequently. From this form of analysis, I determined that
    AAPL_pol was the best baseline feature, followed by MSFT_subj and GE_sdpr.


    |Classifier|Mean AUC|% Increase|
    |---|---|---|
    |Random Forest Baseline|0.497052284352|-- |
    |Random Forest Model|0.51628400372|+ 3.8691542068 %|
    |Linear SVM Baseline|0.494665484771|--|
    |Linear SVM Model|0.545653627063|+ 10.307600562 %|

    ## Results and Discussion
    The model was run using the the full features matrix with Random Forest and Linear SVM, and compared to the
    baseline. While the Linear SVM for the model had a 10.3% increase in AUC as opposed to the baseline, its AUC of 0.55
    is considered to be a very poor score. A much higher confidence level is required to perform any meaningful
    prediction with the model. This poor score is likely due to incomplete sentiment data, and improper features on the
    model. 


