# This python script concatenates game stats output files into one file
# for easier importing to a database.
#
# Example: python concatgames.py 1 15
#
# Note: This would concatenate g1output.txt to g15output.txt into one 
#       file named games1-15.txt
import sys

args = sys.argv[1:]

start = args[0]
stop = args[1]

outputName = "games" + start + "-" + stop + ".txt"
output = open(outputName, "w")

start = int(start)
stop = int(stop)

i = start
while i <= stop:
    inFile = open("g" + str(i) + "output.txt", "r")
    for line in inFile:
        output.write(line)

    inFile.close()
    output.write("\n")
    i += 1

output.close()
