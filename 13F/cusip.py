#!/usr/bin/env python

if __name__ == "__main__":

    out = open('cusips.txt', 'w')
    for line in list(open('cusip.csv')):
        cols = line.split(",")
        out.write(cols[-1])

