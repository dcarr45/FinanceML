import requests
import json
import sys

#URL_old = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{from_day}%1F{year}%2Ccd_max%3A{month}%2F{to_day}%2F{year}'
URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&tbs=cdr%3A1%2Ccd_min%3A{month1}%2F{day}%1F{year}%2Ccd_max%3A{month2}%2F{day}%2F{year}'

def fmt(term):
    return term.lower() \
        .replace("&","%26") \
        .replace(" ", "+")

def goog_url(**params):
    return URL.format(**params)

if __name__ == '__main__':
	args = sys.argv[1:]
	query,month,day,year = args
	print goog_url(query=fmt(query),month1=month,month2=month,day=day,year=year)
