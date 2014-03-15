# This python file will run the statsparser python script against specific game text files.
# 
# Example: python rungames.py 1 15
#
# Note: This would run the rungames.py script against game files g1.txt to g15.txt 
import sys, os

args = sys.argv[1:]

start = int(args[0])
stop = int(args[1])

i = start
while i <= stop:
    os.system("python statsparser.py g" + str(i) + ".txt")
    #print "\n"
    i += 1

print "finished"
