# This python script creates SQL insert statements for the game table.
#
# Example: python gameparser.py games.txt
import sys

args = sys.argv[1:]

gamesFile = open(args[0], "r")
fileToParse = args[0].replace('.txt', '')
outFile = open(fileToParse + "output.txt", "w")

# Read in team file and load into dictionary
teamDict = dict()
teamFile = open("teamdictionary.txt", "r")
for line in teamFile:
    firstSpace = line.find(" ")
    teamNum = line[:3]
    teamName = line[4:].strip().lower().replace(' ', '')
    #print "team: ", teamName, " index: ", teamNum
    teamDict[teamName] = teamNum

monthDict = dict()
monthDict['Jan'] = "01"
monthDict['Feb'] = "02"
monthDict['Mar'] = "03"
monthDict['Apr'] = "04"
monthDict['May'] = "05"
monthDict['Jun'] = "06"
monthDict['Jul'] = "07"
monthDict['Aug'] = "08"
monthDict['Sep'] = "09"
monthDict['Oct'] = "10"
monthDict['Nov'] = "11"
monthDict['Dec'] = "12"

def determineTeamName(name):
    """
    This function fixes discrepancies between game file team names and database team name
    """
    if name == "southerncalifornia":
        return 'usc'
    elif name == "louisianastate":
        return 'lsu'
    elif name == "texaschristian":
        return 'tcu'
    elif name == 'mississippi':
        return 'olemiss'
    elif name == 'miami(fl)':
        return 'miamifl'
    elif name == 'centralflorida':
        return 'ucf'
    elif name == "bowlinggreenstate":
        return 'bowlinggreen'
    elif name == "middletennesseestate":
        return "middletennessee"
    elif name == "northcarolinastate":
        return "ncstate"
    elif name == "texas-sanantonio":
        return 'utsa'
    elif name == "westernkentucky":
        return "wku"
    elif name == "brighamyoung":
        return "byu"
    elif name == "southernmethodist":
        return "smu"
    elif name == "nevada-lasvegas":
        return "unlv"
    elif name == "texas-elpaso":
        return "utep"
    elif name == "alabama-birmingham":
        return "uab"
    elif name == "floridainternational":
        return "fiu"
    elif name == "massachusetts":
        return "umass"
    elif name == "miami(oh)":
        return "miamioh"
    elif name == "southernmississippi":
        return "southernmiss"
    elif name == "tennessee-martin":
        return "utmartin"
    elif name == "california-davis":
        return "ucdavis"
    elif name == "virginiamilitaryinstitute":
        return "vmi"
    elif name == "citadel":
        return "thecitadel"
    return name

#Rk,Wk,Date,Day,Winner/Tie,Pts,@ for visiting winner or blank for home winner,Loser/Tie,Pts,Notes
cnt = 0
gameToWrite = "INSERT INTO game VALUES "
for line in gamesFile:
    if line[0:2] == "Rk":
        continue
    if line[0:1] == "#":
        continue
    splitLine = line.strip().split(',')
    gid = int(splitLine[0])
    week = int(splitLine[1])
    spacedDate = splitLine[2]
    splitDate = spacedDate.split()
    gdate = splitDate[2] + "-" + monthDict[splitDate[0]] + "-" + splitDate[1]
    hometeam, homescore, homeresult, homerank = 0, 0, '', 0
    awayteam, awayscore, awayresult, awayrank = 0, 0, '', 0
    name = ""
    if splitLine[4][0:1] == '(':
        # Team is ranked (i.e. (2) Oregon)
        firstSpace = splitLine[4].find(' ')
        name = splitLine[4][firstSpace:].lower().replace(' ', '')
    else:
        name = splitLine[4].lower().replace(' ', '')
    name = determineTeamName(name)
    #print 'Name: ' + name + ' with id of ' + teamDict[name] + ' with ranking of ' + splitLine[4][1:splitLine[4].find(')')]
    
    if splitLine[6] == '@':
        # Winning team was away team
        awayteam = int(teamDict[name])
        awayscore = splitLine[5]
        awayresult = 'W'
        if splitLine[4][0:1] == '(':
            awayrank = int(splitLine[4][1:splitLine[4].find(')')])
    else:
        # Winning team was home team
        hometeam = int(teamDict[name])
        homescore = splitLine[5]
        homeresult = 'W'
        if splitLine[4][0:1] == '(':
            homerank = int(splitLine[4][1:splitLine[4].find(')')])
    
    name = ""
    if splitLine[7][0:1] == '(':
        # Team is ranked
        firstSpace = splitLine[7].find(' ')
        name = splitLine[7][firstSpace:].lower().replace(' ', '')
    else:
        name = splitLine[7].lower().replace(' ', '')
    name = determineTeamName(name)
    #print 'Name: ' + name + ' with id of ' + teamDict[name] + ' with ranking of ' + splitLine[4][1:splitLine[4].find(')')]
    
    if splitLine[6] == '@':
        # Winning team was away team
        hometeam = int(teamDict[name])
        homescore = splitLine[8]
        homeresult = 'L'
        if splitLine[7][0:1] == '(':
            homerank = int(splitLine[7][1:splitLine[7].find(')')])
    else:
        # Winning team was home team
        awayteam = int(teamDict[name])
        awayscore = splitLine[8]
        awayresult = 'L'
        if splitLine[7][0:1] == '(':
            awayrank = int(splitLine[7][1:splitLine[7].find(')')])
    
    notes = splitLine[9]
    
    gameToWrite += "(" + str(gid) + "," + str(week) + ",\'" + gdate + "\'," + str(hometeam) + "," + str(homescore) + ",\'" + homeresult + "\'," + str(homerank) + "," + str(awayteam) + "," + str(awayscore) + ",\'" + awayresult + "\'," + str(awayrank) + ",\'" + notes + "\'),"
    if cnt == 30:
        print gameToWrite
    cnt += 1
	
#print gameToWrite[:-1]
outFile.write(gameToWrite[:-1])
outFile.write(";")

gamesFile.close()
outFile.close()
teamFile.close()
