import urllib2
import pytz
from datetime import datetime
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    global d,isLeague,gameNum
    d = ''
    isLeague = False
    gameNum = -1
    def handle_starttag(self,tag,attrs):
        global isLeague,gameNum,d
        for attr in attrs:
            if(attr[1]=='league'):
                isLeague=True;
            if(attr[1]=='live_scorebox'):
                gameNum += 1
                d+='\n'
                


    def handle_data(self, data):
        global d,isLeague,gameNum
        if(data.find('*')>0):
            gameNum=-1
            return
        if(isLeague):
            isLeague = False
            d += '|**' + data + '**|'
            return (data)
        if(gameNum>0):
            data = data.lstrip("\n")
            data = data.strip(" ")
            if(len(data)>0):
                d += data + '!'
            
    def return_data(self):
        global d
        return d
        
def getFlair(team):
    flairFormat=team.replace(" ","").lower()
    flairFormat=flairFormat.replace("-","").lower()
    flairFormat=flairFormat.replace(".","").lower()
    dict = {"American Int'l": "americaninternational",
         "asu": "arizonastate",
         "Ala.-Huntsville": "uah",
         "Minnesota State": "mankatostate",
         "Northern Mich." : "northernmichigan",
         "Miami" : "miamioh",
         "Lake Superior" : "lakesuperiorstate",
         "Alaska" : "alaskafairbanks",
         "Rensselaer" : "rpi2",
         "Massachusetts" : "umass",
         "Mass.-Lowell": "massachusettslowell"
         }
    if team in dict:
        flairFormat = dict[team]
    if team == 'asu':
        team = "Arizona State"
    if team == "Rensselaer":
        team = "RPI"
    if team == "Massachusetts":
        team = "UMass"
    if team == "Mass.-Lowell":
        team = "UMass-Lowell"
    return "[{}](#f/{}){}".format(team,flairFormat,team)
    
       
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

url = "http://scoreboard.uscho.com"
f=urllib2.urlopen(url)
html = f.read()
f.close()
parser.feed(html)
gameData=parser.return_data()
gameData = gameData.split("|")
gameData.pop(0)
gameData.pop()
gameData.pop()

# Pre-Game/Final
#game[0] - Home Team
#game[1] - Home Score
#game[2] - Start Time/Final
#game[3] - Away Team
#game[4] - Away Score

# Mid-Game
#game[0] - Home Team
#game[1] - Home Score
#game[2] - Time in Per
#game[3] - Period
#game[4] - Away Team
#game[5] - Away Score

gameId = 0;
leagueList = [];
gamesList = []; 
leagueName = '';   
for league in gameData:
    league=league.lstrip('\n');
    games=league.split('\n')
    for game in games:
        game=game.split('!')
        if(len(game)>1):
            
            game.pop()
            if(len(game)==5):
              gameDict={"gameId": gameId,
                        "league": leagueName,
                        "homeTeam" : game[0],
                        "homeScore" : game[1],
                        "awayTeam": game[3],
                        "awayScore": game[4],
                        "time": game[2]}
              gameId+=1
            elif(len(game)==6):
              time = "P"+game[3]+" " + game[2]
              gameDict={"gameId": gameId,
                        "league": leagueName,
                        "homeTeam" : game[0],
                        "homeScore" : game[1],
                        "awayTeam": game[4],
                        "awayScore": game[5],
                        "time": time}
              gameId+=1
            elif(len(game)==4):
              gameDict={"gameId": gameId,
                        "league": leagueName,
                        "homeTeam" : game[0],
                        "homeScore" : game[1],
                        "awayTeam": game[2],
                        "awayScore": game[3],
                        "time": ""}
                
              gameId+=1
            gamesList.append(gameDict)
        else:
            leagueName = game[0]
            leagueList.append(leagueName)
            
for league in leagueList:
    print league
    print "\n|Away|Away Score|Home|Home Score|Time\n|---|---|---|---|---|"
    for game in gamesList:
        if(game["league"] == league):
            print "{}|{}|{}|{}|{}|".format(getFlair(game["awayTeam"]), game["awayScore"], getFlair(game["homeTeam"]), game["homeScore"], game["time"])          

    




