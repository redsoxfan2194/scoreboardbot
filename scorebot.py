import urllib2
import pytz
from datetime import datetime
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    global d, startParse, eol
    d = ''
    startParse = False
    eol = False
    def handle_starttag(self, tag, attrs):
        global startParse,eol
        eol = False
        for attr in attrs:
            if(attr[1]=='chsschedreg'):
                startParse=True;
        pass

    def handle_endtag(self, tag):
        global d
        if(startParse and tag=='tr'):
            d+='\n'

    def handle_data(self, data):
        global d,startParse
        if(startParse):
            data=data.lstrip('\n')
            if(data != 'Box' and data != 'Text' and data !=' / ' and data != 'Live - '):
                if(data == 'Sheet'):
                    d += 'Final!'
                else:
                    d += data + '!'

    def return_data(self):
        global d
        return d

def getLeagueName(name):
    leagueNames={'WC': "WCHA",
                 'AH': "Atlantic Hockey",
                 'NC': "Non-Conference",
                 'B1': "Big Ten",
                 'EC': "ECAC",
                 'NH': "NCHC",
                 'HE': "Hockey East",
                 'CH': "College Hockey America",
                 'EX': "Exhibition",
                 'NW': "NEWHA"}
    if name not in leagueNames.keys():
        return 'N/A'
    return leagueNames[name]
def isD1(team1,team2,m_w):
    validMTeams = ["Air Force","Alabama Huntsville","Alaska","Alaska Anchorage","American International","Arizona State","Army","Bemidji State","Bentley","Boston College","Boston University","Bowling Green","Brown","Canisius","Clarkson","Colgate","Colorado College","Connecticut","UConn","Cornell","Dartmouth","Denver","Ferris State","Harvard","Holy Cross","Lake Superior State","Maine","Massachusetts","Mercyhurst","Merrimack","Miami","Michigan","Michigan State","Michigan Tech","Minnesota","Minnesota Duluth","Minnesota State","New Hampshire","Niagara","North Dakota","Northeastern","Northern Michigan","Notre Dame","Ohio State","Omaha","Penn State","Princeton","Providence","Quinnipiac","Rensselaer","RIT","Robert Morris","Sacred Heart","St. Cloud State","St. Lawrence","UMass Lowell","Union","Vermont","Western Michigan","Wisconsin","Yale"]
    validWTeams = ["Bemidji State","Boston College","Boston University","Brown","Clarkson","Colgate","Connecticut", "UConn","Cornell","Dartmouth","Franklin Pierce","Harvard","Holy Cross","Lindenwood","Maine","Mercyhurst","Merrimack","Minnesota","Minnesota Duluth","Minnesota State","New Hampshire","Northeastern","Ohio State","Penn State","Post","Princeton","Providence","Quinnipiac","Rensselaer","RIT","Robert Morris","Sacred Heart","Saint Anselm","Saint Michael's","St. Cloud State","St. Lawrence","Syracuse","Union","Vermont","Wisconsin","Yale"]
    if(m_w == 'Men' and (team1 in validMTeams or team2 in validMTeams)):
        return True
    if(m_w == 'Women' and (team1 in validWTeams or team2 in validWTeams)):
        return True
    return False
        
def getFlair(team):
    flairFormat=team.replace(" ","").lower()
    flairFormat=flairFormat.replace("-","").lower()
    flairFormat=flairFormat.replace(".","").lower()
    dict = {"American Int'l": "americaninternational",
         "asu": "arizonastate",
         "Alabama Huntsville": "uah",
         "Minnesota State": "mankatostate",
         "Northern Mich." : "northernmichigan",
         "Miami" : "miamioh",
         "Lake Superior" : "lakesuperiorstate",
         "Alaska" : "alaskafairbanks",
         "Rensselaer" : "rpi2",
         "Massachusetts" : "umass",
         "UMass Lowell": "massachusettslowell",
         "UConn": "connecticut",
         "Omaha": "nebraskaomaha",
         "Army West Point": "army",
         "Saint Anselm" : "stanselm",
         "Saint Michael's" : "stmichaels"
         }
    if team in dict:
        flairFormat = dict[team]
    if team == 'asu':
        team = "Arizona State"
    if team == "Rensselaer":
        team = "RPI"
    if team == "Massachusetts":
        team = "UMass"
    
    return "[](#f/{}){}".format(flairFormat,team)    
# instantiate the parser and fed it some HTML
   
def getScores():
    global gameDate,gameList
    parser = MyHTMLParser()

    url = "http://collegehockeystats.net/"
    f=urllib2.urlopen(url)
    html = f.read()
    f.close()
    parser.feed(html)
    
    if("<meta HTTP-EQUIV=\"REFRESH\"" in html):
        url=html.split("url=")
        url=url[1].split("\"")[0]
        f=urllib2.urlopen(url)
        html = f.read()
        f.close()
        parser.feed(html)
    gameData=parser.return_data()
    days = gameData.split('\n\n')
    games = days[0].split('\n')
    mtagLookup = {}
    wtagLookup = {}
    leagues=set()
    gameList = []
    tag = ''
    #print gameData
    for game in games:
        game = game.split('!')
        if(len(game)==1):
            continue
        if(game[0]==''):
            game.pop(0)

        if(game[-1]==''):
            game.pop()
            if(game==[]):
                break
            try:
                if(game[-1][0]=='('):
                    game.pop()
            except IndexError:
                pass
        if(len(game)==2):
           if(game[0][0]=='('):
               
               if(m_w=='Men'):
                   mtagLookup[game[0]]=game[1]
               elif(m_w=='Women'):
                   wtagLookup[game[0]]=game[1]
           else:
               m_w = game[1][:-1]
               gameDate = game[0][:-3]
               gameDate=gameDate.replace(",","")
               
        if(len(game)>2):
            if(game[0][0]=='('):
                tag=game[0]
                game.pop(0)
        
        if(game.count('OT')>0):
            game.pop(5)
            if(game.count('Final')>0):
                game[7]='Final (OT)'
        if(len(game)==8):
            if(game[5]=='EC,IV'):
               game[5] = 'EC'
            if(m_w == 'Women' and game[5]=='NH'):
              game[5] = 'NW'           
            gameDict = {'awayTeam' : game[0],
                        'awayScore': game[1],
                        'homeTeam' : game[3],
                        'homeScore': game[4],
                        'league' : game[5],
                        'startTime': game[6],
                        'status' : game[7],
                        'm_w': m_w}
            leagues.add(game[5])
            gameList.append(gameDict)
        if(len(game)==9):
          if(game[5]=='EC,IV'):
            game[5] = 'EC'
          if(m_w == 'Women' and game[5]=='NH'):
              game[5] = 'NW'
          if(tag):
            if(m_w=='Men' and tag in mtagLookup.keys()):
              game[5]=mtagLookup[tag]
            if(m_w=='Women' and tag in wtagLookup.keys()):
               game[5]=wtagLookup[tag]
          time = game[8] + ' ' + game[7]
          gameDict = {  'awayTeam' : game[0],
                        'awayScore': game[1],
                        'homeTeam' : game[3],
                        'homeScore': game[4],
                        'league' : game[5],
                        'startTime': game[6],
                        'status' : time,
                        'm_w' : m_w}
          leagues.add(game[5])
          gameList.append(gameDict)
        if(len(game)==5):
            if(game[3]=='EC,IV'):
              game[3] = 'EC'
            if(m_w == 'Women' and game[3]=='NH'):
              game[3] = 'NW'
            gameDict = {'awayTeam' : game[0],
                        'awayScore': "",
                        'homeTeam' : game[2],
                        'homeScore': "",
                        'league' : game[3],
                        'startTime': "",
                        'status' : game[4],
                        'm_w': m_w}
            leagues.add(game[3])
            gameList.append(gameDict)
def generateScoreboard():
    global gameList
    getScores()
    mGamesByLeague = {}
    wGamesByLeague = {}
    for game in gameList:
        if(not isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
            continue
        if game['m_w'] == 'Men':
            if(game['league'] not in mGamesByLeague):
                mGamesByLeague[game['league']]=[]
            mGamesByLeague[game['league']].append(game)
        if game['m_w'] == 'Women':
            if(game['league'] not in wGamesByLeague):
                wGamesByLeague[game['league']]=[]
            wGamesByLeague[game['league']].append(game)
            
    scoreboard = ''
    scoreboard += "#Men's Scores\n"
    numGames = 0
    for league in sorted(mGamesByLeague.keys()):
        scoreboard += "**{}**\n".format(getLeagueName(league))
        scoreboard += "\n|Away|Away Score|Home|Home Score|Time\n|---|---|---|---|---|\n"
        for game in mGamesByLeague[league]:
            if(isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
                scoreboard += "{}|{}|{}|{}|{}|\n".format(getFlair(game["awayTeam"]), game["awayScore"], getFlair(game["homeTeam"]), game["homeScore"], game['status'])
                numGames +=1
    if(numGames==0):
        scoreboard=scoreboard.replace("#Men's Scores\n","")
    
    numGames = 0
    scoreboard += "#Women's Scores\n"
    for league in sorted(wGamesByLeague.keys()):
        scoreboard += "**{}**\n".format(getLeagueName(league))
        scoreboard +=  "\n|Away|Away Score|Home|Home Score|Time\n|---|---|---|---|---|\n"
        for game in wGamesByLeague[league]:
          if(isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
            scoreboard += "{}|{}|{}|{}|{}|\n".format(getFlair(game["awayTeam"]), game["awayScore"], getFlair(game["homeTeam"]), game["homeScore"], game['status'])        
            numGames += 1
    if(numGames == 0):
        scoreboard=scoreboard.replace("#Women's Scores\n","")

    return scoreboard
    
if __name__ == '__main__':
    global gameDate
    scoreboard=generateScoreboard()
    #getScores()
    print scoreboard
