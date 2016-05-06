#getYahooAPIData.py


# sudo -H pip install yahoo-finance

from yahoo_finance import Share
from pprint import pprint

yahoo = Share('YHOO')

start = '2015-01-01'
end = '2015-12-31'
yahoo_prices = yahoo.get_historical(start,end)
yahoo_info = yahoo.get_info()
print type(yahoo_prices)

print yahoo_prices[0]


# Methods

# get_price()
# get_change()
# get_volume()
# get_prev_close()
# get_open()
# get_avg_daily_volume()
# get_stock_exchange()
# get_market_cap()
# get_book_value()
# get_ebitda()
# get_dividend_share()
# get_dividend_yield()
# get_earnings_share()
# get_days_high()
# get_days_low()
# get_year_high()
# get_year_low()
# get_50day_moving_avg()
# get_200day_moving_avg()
# get_price_earnings_ratio()
# get_price_earnings_growth_ratio()
# get_price_sales()
# get_price_book()
# get_short_ratio()
# get_trade_datetime()
# get_historical(start_date, end_date)
# get_info()
# refresh()
