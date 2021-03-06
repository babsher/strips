#! /usr/bin/python

import sys
import re
from sets import Set

filename = sys.argv[1]
outFilename = sys.argv[2]
print 'Generating problem for file: {}'.format(filename)
print 'Writing to file: {}'.format(outFilename)

file = open(filename)
out = open(outFilename, 'w')

robot = {}
open = set()
blocked = set()
box = set()
goal = set()

row = 0
col = 0
lines = file.readlines()
for line in lines:
    col = 0
    entries = re.split('\s+', line)
    for entry in entries:
        if entry != '':
            print '{0} at ({1},{2})'.format(entry, row, col)
            entry = entry.upper()
            m = re.match('R(\d)', entry)
            if entry == '1' or entry == 'X':
                blocked.add((row, col))
            elif m:
                robot[(row, col)] = 'robot-{}'.format(m.group(0))
            elif entry == 'O':
                open.add((row, col))
            elif entry == 'B':
                box.add((row, col))
            elif entry == 'E':
                goal.add((row, col))
            else:
                print 'Unknown: {}'.format(entry)
            col += 1
    row += 1

positions = set(robot.keys()) | blocked | box | goal | open

def printPat(keys, pat):
    for pos in keys:
        out.write(pat.format(pos))

def printLoc(keys):
    printPat(keys, "    pos-{0[0]}-{0[1]} - location\n")
    
def printNonGoal(keys):
    printPat(keys, "    (IS-NONGOAL pos-{0[0]}-{0[1]})\n")

def printMoves(keys):
    for key in keys:
        if not key in blocked:
            up = (key[0]+1,key[1])
            down = (key[0]-1, key[1])
            left = (key[0], key[1]-1)
            right = (key[0], key[1]+1)
            if (not up in blocked) and (up in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-up)\n'.format(key, up))
            if (not down in blocked) and (down in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-down)\n'.format(key, down))
            if (not left in blocked) and (left in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-left)\n'.format(key, left))
            if (not right in blocked) and (right in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-right)\n'.format(key, right))

out.write("(define (problem p012-microban-sequential)\n  (:domain sokoban-sequential)\n  (:objects")
out.write("    dir-down - direction\n")
out.write("    dir-left - direction\n")
out.write("    dir-right - direction\n")
out.write("    dir-up - direction\n")

i = 0
for r in robot.items():
    out.write("    {0[1]} - player\n".format(r))
i = 0
for b in box:
    i = i + 1
    out.write("    stone-{:0>2} - stone\n".format(i))

printLoc(robot)
printLoc(box)
printLoc(open)
printLoc(goal)

out.write("  )  \n(:init\n")

printPat(goal, "    (IS-GOAL pos-{0[0]}-{0[1]})\n")
printNonGoal(robot)
printNonGoal(box)
printNonGoal(open)

printMoves(positions)

i = 0
for b in box:
    i = i + 1
    out.write("    (at stone-{0:0>2} pos-{1[0]}-{1[1]})\n".format(i, b))

for p in positions - blocked:
    out.write("    (clear pos-{0[0]}-{0[1]})\n".format(p))
        
for (k, r) in robot.items():
    out.write("    (at {0} pos-{1[0]}-{1[1]})\n".format(r, k))

out.write('  )\n  (:goal (and\n')

i = 0
for b in box:
    i = i + 1
    out.write("    (at-goal stone-{:0>2})\n".format(i))
out.write('    )\n  )\n)'.format())