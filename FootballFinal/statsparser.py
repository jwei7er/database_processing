# This python script creates SQL insert statements for the 8 different
# stats tables by reading in a text file containing CSV stat information
# for a game and creating the necessary SQL statements.
#
# Example: python statsparser.py g810.txt
import sys

args = sys.argv[1:]

gameFile = open(args[0], "r")
fileToParse = args[0].replace('.txt', '')
outFile = open(fileToParse + "output.txt", "w")

# Game file in the format of g#.txt
gameId = args[0][1:args[0].find('.')]
#print "Calculating game number as " + gameId

loadedRosterDict = dict()
playerDict = dict()

# Load teams into dictionary
teamFile = open("teamdictionary.txt", "r")
teamDict = dict()
for line in teamFile:
    firstSpace = line.find(" ")
    teamNum = line[:3]
    teamName = line[4:].strip().lower().replace(' ', '')
    teamDict[teamName] = teamNum

def determineTeamName(teamName):
    """
    This function fixes discrepancies between team names in stats files and team names in the database.
    """
    if teamName == "southerncalifornia":
        return 'usc'
    elif teamName == "louisianastate":
        return 'lsu'
    elif teamName == "texaschristian":
        return 'tcu'
    elif teamName == 'mississippi':
        return 'olemiss'
    elif teamName == 'miami(fl)':
        return 'miamifl'
    elif teamName == 'centralflorida':
        return 'ucf'
    elif teamName == "bowlinggreenstate":
        return 'bowlinggreen'
    elif teamName == "middletennesseestate":
        return "middletennessee"
    elif teamName == "northcarolinastate":
        return "ncstate"
    elif teamName == "texas-sanantonio":
        return 'utsa'
    elif teamName == "westernkentucky":
        return "wku"
    elif teamName == "brighamyoung":
        return "byu"
    elif teamName == "southernmethodist":
        return "smu"
    elif teamName == "nevada-lasvegas":
        return "unlv"
    elif teamName == "texas-elpaso":
        return "utep"
    elif teamName == "alabama-birmingham":
        return "uab"
    elif teamName == "floridainternational":
        return "fiu"
    elif teamName == "massachusetts":
        return "umass"
    elif teamName == "miami(oh)":
        return "miamioh"
    elif teamName == "southernmississippi":
        return "southernmiss"
    elif teamName == "tennessee-martin":
        return "utmartin"
    elif teamName == "california-davis":
        return "ucdavis"
    elif teamName == "virginiamilitaryinstitute":
        return "vmi"
    elif teamName == "citadel":
        return "thecitadel"
    return teamName


cnt = 0
#gameId = 0
teamId = 0
playerId = 0
statsToWrite = "INSERT INTO game VALUES "
passingStatsToWrite = "INSERT INTO passingstats VALUES "
rushingStatsToWrite = "INSERT INTO rushingstats VALUES "
receivingStatsToWrite = "INSERT INTO receivingstats VALUES "
defensiveStatsToWrite = "INSERT INTO defensivestats VALUES "
kickReturnStatsToWrite = "INSERT INTO kickreturnstats VALUES "
puntReturnStatsToWrite = "INSERT INTO puntreturnstats VALUES "
kickingStatsToWrite = "INSERT INTO kickingstats VALUES "
puntingStatsToWrite = "INSERT INTO puntingstats VALUES "

passStat = False
rushStat = False
recStat = False
defStat = False
kretStat = False
pretStat = False
kickStat = False
puntStat = False

foundAllPlayers = True
missingPlayers = ""
skipLines = 0
for line in gameFile:
    #print line
    if skipLines > 0:
        skipLines -= 1
        continue
    elif line[0:2] == "Rk":
        continue
    elif line.strip() == "":
        continue
    elif line[0:11] == "Reload page" or line[0:9] == "Rushing &" or line[0:9] == "Defense &" or line[0:6] == "Kick &" or line[0:9] == "Kicking &":
        continue
    elif line[0:1] == "#":
        continue
    elif line[0:2] == ",,":
        passStat = False
        rushStat = False
        recStat = False
        defStat = False
        kretStat = False
        pretStat = False
        kickStat = False
        puntStat = False

        splitLine = line.strip().split(',')
        if splitLine[2] == "Passing":
            passStat = True
            skipLines = 1
            continue

        elif splitLine[2] == "Rushing":
            rushStat = True
            recStat = True
            skipLines = 1
            continue

        elif splitLine[2] == "Tackles":
            defStat = True
            skipLines = 1
            continue

        elif splitLine[2] == "Kick Ret":
            kretStat = True
            pretStat = True
            skipLines = 1
            continue

        elif splitLine[2] == "Kicking":
            kickStat = True
            puntStat = True
            skipLines = 1
            continue
    else:
        splitLine = line.strip().split(',')
        if len(splitLine) < 4:
            #print "ERROR!!! Line does not have commas: ", line
            continue
        playerId = 0
        playerName = splitLine[0]
        teamName = splitLine[1].lower().replace(' ', '')
        teamName = determineTeamName(teamName)
        teamId = int(teamDict[teamName])
        if teamName in loadedRosterDict.keys():
            cnt = 0
        else:
            # & in TA&M was causing issues with file names
            if teamName == "texasa&m":
                teamName = "texasa_m"	

            # Load team's roster into a dictionary
            rosterFile = open("FinishedRosters/" + teamName + "output.txt", "r")
            for rLine in rosterFile:
                # Players are divided by parentheses
                rSplit = rLine.split('),(')
                for l in rSplit:
                    if "INSERT" in l:
                        line = l[l.find(" (") + 2:]
                    else:
                        line = l
                    lSplit = line.split(',')
                    pid = int(lSplit[0])
                    fname = lSplit[1][1:-1].replace("\\'","\'").replace(" ","")
                    lname = lSplit[2][1:-1].replace("\\'","\'").replace(" ","")
                    playerDict[fname.lower() + lname.lower()] = pid
        
            loadedRosterDict[teamName] = True
            rosterFile.close()

        pnSplit = playerName.lower().split()
        # Try to remove condense player's name by removing suffixes
        if len(pnSplit) > 2 and (pnSplit[-1] == "sr." or pnSplit[-1] == "jr." or pnSplit[-1] == "jr" or pnSplit[-1] == "ii" or pnSplit[-1] == "iii" or pnSplit[-1] == "iv"):
            pnCondense = "".join(pnSplit[:-1])
        else:
            pnCondense = "".join(pnSplit)
        if pnCondense in playerDict:
            playerId = playerDict[pnCondense]
        else:
            playerId = 0
            foundAllPlayers = False
            missingPlayers += "\n" + playerName + " from " + teamName + " not found in dictionary"

        if passStat:
            cmp = int(splitLine[2])
            att = int(splitLine[3])
            yds = int(splitLine[5])
            tds = int(splitLine[8])
            ints = int(splitLine[9])
            rate = float(splitLine[10])
    
            if playerId > 0:
                passingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(cmp) + "," + str(att) + "," + str(yds) + "," + str(tds) + "," + str(ints) + "),"
            else:
                passingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(cmp) + "," + str(att) + "," + str(yds) + "," + str(tds) + "," + str(ints) + "),"
        if rushStat:
            if len(splitLine[2]) > 0:
                att = int(splitLine[2]) if len(splitLine[2]) > 0 else 0
                yds = int(splitLine[3]) if len(splitLine[3]) > 0 else 0
                tds = int(splitLine[5]) if len(splitLine[5]) > 0 else 0
        
                if playerId > 0:
                    rushingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(att) + "," + str(yds) + "," + str(tds) + "),"
                else:
                    rushingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(att) + "," + str(yds) + "," + str(tds) + "),"
        if recStat:
            if len(splitLine[6]) > 0:
                rec = int(splitLine[6]) if len(splitLine[6]) > 0 else 0
                yds = int(splitLine[7]) if len(splitLine[7]) > 0 else 0
                tds = int(splitLine[9]) if len(splitLine[9]) > 0 else 0
    
                if playerId > 0:
                    receivingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(rec) + "," + str(yds) + "," + str(tds) + "),"
                else:
                    receivingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(rec) + "," + str(yds) + "," + str(tds) + "),"
        if defStat:
            solo = int(splitLine[2]) if len(splitLine[2]) > 0 else 0
            ast = int(splitLine[3]) if len(splitLine[3]) > 0 else 0
            #tot = int(splitLine[4]) if len(splitLine[4]) > 0 else 0
            loss = float(splitLine[5]) if len(splitLine[5]) > 0 else 0
            sack = float(splitLine[6]) if len(splitLine[6]) > 0 else 0
            ints = int(splitLine[7]) if len(splitLine[7]) > 0 else 0
            yds = int(splitLine[8]) if len(splitLine[8]) > 0 else 0
            inttd = int(splitLine[10]) if len(splitLine[10]) > 0 else 0
            pdef = int(splitLine[11]) if len(splitLine[11]) > 0 else 0
            fr = int(splitLine[12]) if len(splitLine[12]) > 0 else 0
            fryds = int(splitLine[13]) if len(splitLine[13]) > 0 else 0
            frtds = int(splitLine[14]) if len(splitLine[14]) > 0 else 0
            ff = int(splitLine[15]) if len(splitLine[15]) > 0 else 0
    
            if playerId > 0:
                defensiveStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(solo) + "," + str(ast) + "," + str(loss) + "," + str(sack) + "," + str(ints) + "," + str(yds) + "," + str(inttd) + "," + str(pdef) + "," + str(fr) + "," + str(fryds) + "," + str(frtds) + "," + str(ff) + "),"
            else:
                defensiveStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(solo) + "," + str(ast) + "," + str(loss) + "," + str(sack) + "," + str(ints) + "," + str(yds) + "," + str(inttd) + "," + str(pdef) + "," + str(fr) + "," + str(fryds) + "," + str(frtds) + "," + str(ff) + "),"
        if kretStat:
            if len(splitLine[2]) > 0:
                ret = int(splitLine[2])
                yds = int(splitLine[3])
                td = int(splitLine[5])
        
                if playerId > 0:
                    kickReturnStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(ret) + "," + str(yds) + "," + str(tds) + "),"
                else:
                    kickReturnStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(ret) + "," + str(yds) + "," + str(tds) + "),"
        if pretStat:
            if len(splitLine[6]) > 0:
                ret = int(splitLine[6])
                yds = int(splitLine[7])
                td = int(splitLine[9])
        
                if playerId > 0:
                    puntReturnStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(ret) + "," + str(yds) + "," + str(tds) + "),"				
                else:
                    puntReturnStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(ret) + "," + str(yds) + "," + str(tds) + "),"
        if kickStat:
            if len(splitLine[3]) > 0 or len(splitLine[6]) > 0:
                xpm = int(splitLine[2]) if len(splitLine[2]) > 0 else 0
                xpa = int(splitLine[3]) if len(splitLine[3]) > 0 else 0
                fgm = int(splitLine[5]) if len(splitLine[5]) > 0 else 0
                fga = int(splitLine[6]) if len(splitLine[6]) > 0 else 0
                pts = int(splitLine[8]) if len(splitLine[8]) > 0 else 0
        
                if playerId > 0:
                    kickingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(xpm) + "," + str(xpa) + "," + str(fgm) + "," + str(fga) + "," + str(pts) + "),"
                else:
                    kickingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(xpm) + "," + str(xpa) + "," + str(fgm) + "," + str(fga) + "," + str(pts) + "),"
        if puntStat:
            if len(splitLine[9]) > 0:
                punts = int(splitLine[9])
                yds = int(splitLine[10])
        
                if playerId > 0:
                    puntingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerId) + "," + str(punts) + "," + str(yds) + "),"
                else:
                    puntingStatsToWrite += "\n(" + str(gameId) + "," + str(teamId) + "," + str(playerName) + "," + str(punts) + "," + str(yds) + "),"

if not foundAllPlayers:
    # Print players who weren't found on a team's roster for specific games
    print str(gameId) + " " + missingPlayers

outFile.write(passingStatsToWrite[:-1] + ";\n\n")
outFile.write(rushingStatsToWrite[:-1] + ";\n\n")
outFile.write(receivingStatsToWrite[:-1] + ";\n\n")
outFile.write(defensiveStatsToWrite[:-1] + ";\n\n")
outFile.write(kickReturnStatsToWrite[:-1] + ";\n\n")
outFile.write(puntReturnStatsToWrite[:-1] + ";\n\n")
outFile.write(kickingStatsToWrite[:-1] + ";\n\n")
outFile.write(puntingStatsToWrite[:-1] + ";\n\n")

gameFile.close()
outFile.close()
teamFile.close()
