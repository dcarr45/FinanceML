#!/usr/bin/env python

from subprocess import call
import sys
import os
import re


if __name__ == "__main__":

    for dir in os.listdir('.'):
		if not os.path.isfile(dir):
			
			#receives file from stdin
			links = []
			unique_ids = set()

			#since the 13F-HR/A (amendment forms) are last in the file,
			#reverse to add most recent files first and no duplicates
			file = open(dir + '/index.txt')
			
			for line in reversed(list(file)):
				cols = re.split("\s{2,}", line) #two or more spaces

				cik, form, link = cols[2], cols[0], cols[4]

				#check for dups
				if cik not in unique_ids:
					links.append(link)
					unique_ids.add(cik)

			out = open(dir + '/links.txt', 'w')
			
			for link in links:
				path = 'ftp://ftp.sec.gov/' + link
				dest = dir + '/forms'
				out.write(path + '\n')
				


