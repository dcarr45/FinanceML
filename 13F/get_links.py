#!/usr/bin/env python

from subprocess import call
import os
import re


if __name__ == "__main__":

    for dir in os.listdir('.'):
        if not os.path.isfile(dir) and str(dir).startswith('Q'):
            qtr = 'QTR' + dir[1] + '/'
            yr = dir[2:] + '/'
            path = 'ftp://ftp.sec.gov/edgar/full-index/' + yr + qtr + 'form.idx'
            call(['wget', path, '-P', dir])

            links = []
            unique_ids = set()

            ind = open(dir + '/index.txt', 'w')

            for line in open(dir + '/form.idx', 'r').readlines()[10:]:
                if line.split()[0].startswith('13F-HR'):
                    ind.write(line)
            ind.close()

	        #since the 13F-HR/A (amendment forms) are last in the file,
            #reverse to add most recent files first and no duplicates
            file = open(dir + '/index.txt')

            for line in reversed(list(file)):
                cols = re.split("\s{2,}", line) #two or more spaces

                cik, form, link = cols[2], cols[0], cols[len(cols) - 2]

                #check for dups
                if cik not in unique_ids:
                    links.append(link)
                    unique_ids.add(cik)
	    
	        file.close()

            out = open(dir + '/links.txt', 'w')

            for link in links:
                path = 'ftp://ftp.sec.gov/' + link
                dest = dir + '/forms'
                out.write(path + '\n')
