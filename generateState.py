#! /usr/bin/python

import sys
import re

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
    entries = re.split('\s+', line)
    for entry in entries:
        if entry != '':
            print '{0} at ({1},{2})'.format(entry, row, col)
            entry = entry.upper()
            if entry == '1' :
                out.write('Obstacle({0}_{1})'.format(row, col))
            elif entry == 'R1':
                out.write('RobotAt(R1,{0}_{1}), '.format(row, col))
                out.write('Obstacle({0}_{1}), '.format(row, col))
                out.write('IsRobot(R1)'.format(row, col))
            elif entry == 'B':
                out.write('BlockAt({0}_{1})'.format(row, col))
            elif entry == 'O':
                out.write('Open({0}_{1})'.format(row, col))
            elif entry == 'E':
                out.write('End({0}_{1}), '.format(row,col))
                out.write('Open({0}_{1})'.format(row, col))
            else:
                print 'Unknown: {}'.format(entry)

            if col != (len(entries)-1) and entry != '':
                out.write(', ')
            col += 1
    row += 1