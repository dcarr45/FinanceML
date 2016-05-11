nalysis
> *Danny Carr*

Our fundamental analysis was performed by analyzing the 13F forms filed by large institutional money managers from 2000
to 2015, with regard to the SPY S&P 500 ETF, and the ten top performing S&P 500 securities by weight, listed previously.
Every institutional investment manager with total holdings over $100,000,000 must file quarterly reports with the SEC,
consisting of the details the each of their positions. We saw this database of filings as a useful tracking indicator
for the largest players in the market, providing the capability of tracking the aggregate holdings of our chosen
securities across a large time frame. By comparing the fluctuation in holdings of each ticker to its relative
performance over that period, we expected to be able to train a machine learning model for performance prediction. 

## Data Collection

The 13F forms were obtained from the SEC’s FTP database through a series of downloads. There is no large data dump
available from the SEC - rather, they maintain an index file for each quarter of each year, consisting of every form
that was filed that quarter, from 1-A to X-17-5, the company that filed it, and the subsequent location of that form on
the FTP database.

|Form Type|Company Name|                  CIK|        Date Filed|       File Name|
|---|---|---|---|---|
|1-A|         JURRASIC INDUSTRIES, INC.   |1545961| 2012-03-27|    edgar/data/1545961/9999999997-12-004575.txt         |
|1-A|         LYONS BANCORP INC     |         816332 |  2012-03-05|    edgar/data/816332/9999999997-12-002091.txt
|
|1-A/A|      ABCO Energy, Inc.                  |1300938| 2012-03-30   | edgar/data/1300938/9999999997-12-004935.txt
|
|...

The first step in acquiring the the data was to download each of these index files for every relevant quarter, and
extract the links to the 13F forms we desired. However, there are several types of 13F forms that companies must file
with the SEC, only some of which are relevant. The full holdings report is filed under 13F-HR, or 13F-HR/A, indicating
an amended form. Other forms, including 13F-NT (notice), and 13F-CONP (cover page), and their respective -/A forms, are
completely irrelevant. Therefore, I extracted only the 13F-HR and 13F-HR/A forms for each index file, and by parsing the
file in reverse order and tracking the CIKs (unique company identifier) I’d previously encountered, acquired a link to
only the most recent amendment of each company’s 13F holdings report from that quarter.

The next step was to iterate through each of the ~4000 13F links for each quarter, and run a wget to acquire each form
from the SEC FTP server. Each form was around 200KB, with the exception of exceedingly large funds’ forms like
Vanguard’s, whose 13F was 8MB, every quarter. I was able to use the xargs command to run as many parallel downloads as
possible, but downloading 250,000 individual 1 MB forms is a painstaking and time consuming process no matter how you
slice it. You can imagine my frustration when I ran my initial download, having parsed the index file for
line.startswith(“13F”), and ended up with 60000 completely useless 13F-NT notice forms. After downloading each quarter’s
worth of files, I stored them in a corresponding directory on Hadoop on the ACCRE cluster.

## Data Transformation

After acquiring the forms, the next step was to extract the relevant data for each ticker that we were considering. I
accomplished this by creating a Spark job to iterate through the forms for each quarter, use BeautifulSoup to parse the
XML, and extract a tuple of (CUSIP, shares) for every position listed in the form, where CUSIP is the unique stock
identifier, and shares is the total number of shares held by the fund for that CUSIP. Each CUSIP was compared to the
list of CUSIPs we were seeking, and only returned if a match was found. I then used reduceByKey to produce, for each
CUSIP, the total number of funds invested in it, and the total number of shares of that CUSIP held by all funds for that
quarter.

## Feature Construction and Data Labeling

With the data parsed and transformed, I was left with a list of the total number of companies invested and the total
number of shares held by 13F companies for each stock we were considering. The number of funds invested is a useful
feature in itself, but to normalize the total shares held, I compared it to the market cap for that share to get a
percentage held by 13F funds. The final feature matrix could then be constructed using those two features for each of
the 11 securities we were considering. The corresponding label matrix was then constructed with a 1 for the quarter if
the adjusted close price of each stock was greater than the previous quarter’s.

## Model Fitting and Classification
Unfortunately, I was unable to develop a useful ML model using the data I was able to extract. Due to the nature of the
forms downloaded, I was unable to parse the requisite values from any forms prior to 2013, as there was no consistent
format for data entry on the forms. Before the SEC adopted XML for their form submission, each information table on the
13Fs was unique to the company that submitted it. The inconsistent formatting made it difficult to parse and extract the
necessary data, so I ended up with only 10 rows, one for each quarter from Q32013, when XML was adopted, to now. With a
10x33 feature matrix, I was unable to successfully fit my data to any model. 


## Results and Discussion

Data collection proved to be the most difficult part of the fundamental analysis. As one might expect, the SEC does not
maintain a quite as user-friendly of a database as any technical financial tracker, such as Yahoo! Finance and the like. 

I ran into several roadblocks while trying to efficiently download the several hundred thousand files I required. With
Spark fresh in my mind, I attempted to write a Spark job to iterate through the various index files I had parsed, and
use the urllib2 library to download the requisite forms. However, Spark does not allow passing the SparkContext variable
to external partitions, and I was thus unable to store the file I had downloaded. I attempted several other methods of
the storing the file, including using subprocess.call to run a “hadoop fs -put” command, but also to no avail.
Eventually, I decided it wasn’t worth the time to optimize, as I was spending more time writing the program as it would
have taken to individually download each file. 

I regret that I was unable to perform any machine learning on my data. With more time and better work ethic, it’s
possible that I would have been able to parse the forms prior to 2012, but the vast majority of those forms are a
formatting nightmare, especially as you get back towards 2000. Table columns are barely delineated, with inconsistent
ordering, columns running over into each other, random new lines in the middle of table rows, you name it. It definitely
wouldn’t have been impossible, and I even think I could have done it, but it would have been a seriously rough time.

Overall, the 13F forms do not provide a sufficient dataset for machine learning, if only because they are a quarterly
filing. While useful features may be extracted, and the data mining itself is certainly doable, with at most 60 rows
over 15 years, at least for the aggregate techniques we were performing, there is simply not enough data.

