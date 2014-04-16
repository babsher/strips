#! /usr/bin/python

import sys

filename = sys.argv[1]
outFilename = sys.argv[2]
print 'Generating problem for file: {}'.format(filename)
print 'Writing to file: {}'.format(outFilename)

file = open(filename)
out = open(outFilename, 'w')

row = 0
col = 0
for line in file.readlines():
    col = 0
    entries = line.split(' ')
    for entry in entries:
        print '{0} at ({1},{2})'.format(entry, row, col)
        entry = entry.upper()
        if entry == '1' :
            out.write('Obstacle({0}_{1})'.format(row, col))
        elif entry == 'R1':
            out.write('At(R1,{0}_{1})'.format(row, col))
        elif entry == 'B':
            out.write('BlockAt({0}_{1})')
        else:
            print entry
            
        if col != len(entries):
            out.write(', ')
        col += 1
    row += 1