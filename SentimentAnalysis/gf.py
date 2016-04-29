from googlefinance import getQuotes
import json
import sys



def take_tickers(t):
	return json.dumps(getQuotes(t), indent = 2)

def parse_quote(t):
	dic = {}
	tks = take_tickers(t)
	lls = [e.replace(" ","").replace('"',"").replace(',','') for e in tks.split('\n')[2:-2]]
	for e in lls:
		i,v = e.split(':',1)
		dic[i] = v
	return dic


def search(tks):
	print 'Searching for %s' % tks
	raw = take_tickers(tks)
	p = parse_quote(raw)
	for e in p:
		print e + ' : ' + p[e]
	# for r in raw:
	# 	print r
	# 	parse_quote(r)

def lookup(field, tks):
	if field == '_':
		print 'Looking up all fields of {}'.format(tks)
		ret = ''
		dic = parse_quote(tks)
		for key in dic.keys():
			ret += key + " : " + dic[key] + '\n'
		return ret
	else:
		print 'Looking up the {} of {}'.format(field,tks)
		dic = parse_quote(tks)
		return field + " : " + dic[field]

if __name__ == '__main__':
	args = sys.argv[1:]
	field = args[0]
	tickers = args[1]
	print lookup(field,tickers)
