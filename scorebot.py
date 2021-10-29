import pytz
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
global gameDate
import re
gameDate=''
def getLeagueName(name):
    leagueNames={'WC': "WCHA",
                 'AH': "Atlantic Hockey",
                 'NON': "Non-Conference",
                 'B1': "Big Ten",
                 'EC': "ECAC",
                 'NH': "NCHC",
                 'HE': "Hockey East",
                 'CH': "College Hockey America",
                 'EX': "Exhibition",
                 'NW': "NEWHA",
                 'ZZZ' : 'Postponed/Canceled'}
    if name not in leagueNames.keys():
        return 'N/A'
    return leagueNames[name]
def isD1(team1,team2,m_w):
    validMTeams = ["Air Force","Alabama Huntsville","Alaska","Alaska Anchorage","American International","Arizona State","Army","Army West Point","Bemidji State","Bentley","Boston College","Boston University","Bowling Green","Brown","Canisius","Clarkson","Colgate","Colorado College","Connecticut","UConn","Cornell","Dartmouth","Denver","Ferris State","Harvard","Holy Cross","Lake Superior State","Maine","Massachusetts","Mercyhurst","Merrimack","Miami","Michigan","Michigan State","Michigan Tech","Minnesota","Minnesota Duluth","Minnesota State","New Hampshire","Niagara","North Dakota","Northeastern","Northern Michigan","Notre Dame","Ohio State","Omaha","Penn State","Princeton","Providence","Quinnipiac","Rensselaer","RIT","Robert Morris","Sacred Heart","St. Cloud State","St. Lawrence", "St. Thomas","UMass Lowell","Union","Vermont","Western Michigan","Wisconsin","Yale"]
    validWTeams = ["Bemidji State","Boston College","Boston University","Brown","Clarkson","Colgate","Connecticut", "UConn","Cornell","Dartmouth","Franklin Pierce","Harvard","Holy Cross","Lindenwood", "Long Island University","Maine","Mercyhurst","Merrimack","Minnesota","Minnesota Duluth","Minnesota State","New Hampshire","Northeastern","Ohio State","Penn State","Post","Princeton","Providence","Quinnipiac","Rensselaer","RIT","Robert Morris","Sacred Heart","Saint Anselm","Saint Michael's","St. Cloud State","St. Lawrence", "St. Thomas","Syracuse","Union","Vermont","Wisconsin","Yale"]
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
         "Long Island University" : "liu",
         "Long Island" : "liu",
         "Alaska" : "alaskafairbanks",
         "Rensselaer" : "rpi2",
         "Providence" : "providence2",
         "Massachusetts" : "umass",
         "UMass Lowell": "massachusettslowell",
         "Mass Lowell" : "massachusettslowell",
         "Mass.-Lowell" : "massachusettslowell",
         "UConn": "connecticut",
         "Omaha": "nebraskaomaha",
         "Army West Point": "army",
         "Saint Anselm" : "stanselm",
         "Saint Michael's" : "stmichaels",
         "St. Thomas" : "stthomasmn"
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
 

def getScores():
    global gameList,gameDate
    gameList = []
    gameDict={}
    leagues = set()
    genders=['Men','Women']
    for gender in genders:
        if gender=='Men':
            url = "https://www.collegehockeynews.com/schedules/scoreboard.php"
            #url = "https://www.collegehockeynews.com/schedules/scoreboard.php?sd=20211008"
        elif gender == 'Women':
            url = "https://www.collegehockeynews.com/women/scoreboard.php"
            #url = "https://www.collegehockeynews.com/women/scoreboard.php?sd=20211008"
            
        f=urllib.request.urlopen(url,timeout=10)
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'html.parser')
        data =soup.find_all('div',{'class':'confGroup'})

        gameDate = soup.find('p',{'class':'date'}).get_text()

        for conf in data:
            conference=conf.find('h2').get_text()
            games=conf.find_all('table',{'id':'mainscore'})
            gClass=conf.find_all('div',{'class':'game'})
            tvList=[]
            for i in gClass:
                para=i.find_all('p',{'class','meta'})
                if(para==[]):
                     tvList.append(' ')
                else:
                
                    text=para[0].get_text()
                    if('TV' in text):
                        m=re.search('TV: (.*)',text)
                        tvList.append(m.group(1))
                    else:
                        tvList.append(' ')

            
            gCount = 0

            for i in games:          
                gameData=i.find_all('td')
                tv=''
                if(tvList!=[]):
                    tv=tvList[gCount]
                tv=tv.rstrip(' ')
                if(gender=='Men'):
                    gameDict = {'awayTeam' : gameData[2].get_text(),
                    'awayScore': gameData[3].get_text(),
                    'homeTeam' : gameData[7].get_text(),
                    'homeScore': gameData[8].get_text(),
                    'league' : conference,
                    'status' : gameData[4].get_text(separator=" "),
                    'm_w': gender,
                    'tv' : tv}
                elif(gender=='Women'):
                    gameDict = {'awayTeam' : gameData[1].get_text(),
                    'awayScore': gameData[2].get_text(),
                    'homeTeam' : gameData[5].get_text(),
                    'homeScore': gameData[6].get_text(),
                    'league' : conference,
                    'status' : gameData[3].get_text(separator=" "),
                    'm_w': gender,
                    'tv' : tv}
                leagues.add(conference)
                gameList.append(gameDict)
                gCount+=1
                
   
def generateScoreboard():
    global gameList
    getScores()
    mGamesByLeague = {}
    wGamesByLeague = {}
    for game in gameList:
        if(not isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
            continue
        game['status']=game['status'].rstrip(' ');
        if(game['status']=='Canceled' or game['status']=='Postponed'):
            game['league'] = 'ZZZ'
        if(game['league']=='NC'):
            game['league'] = 'NON'
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
        scoreboard += "**{}**\n".format(league)
        scoreboard += "\n|Away|Away Score|Home|Home Score|Time|TV\n|---|---|---|---|---|---|\n"
        for game in mGamesByLeague[league]:
            if(isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
                scoreboard += "{}|{}|{}|{}|{}|{}|\n".format(getFlair(game["awayTeam"]), game["awayScore"], getFlair(game["homeTeam"]), game["homeScore"], game['status'],game['tv'])
                numGames +=1
    if(numGames==0):
        scoreboard=scoreboard.replace("#Men's Scores\n","")
    
    numGames = 0
    scoreboard += "#Women's Scores\n"
    for league in sorted(wGamesByLeague.keys()):
        scoreboard += "**{}**\n".format(league)
        scoreboard +=  "\n|Away|Away Score|Home|Home Score|Time|TV\n|---|---|---|---|---|---|\n"
        for game in wGamesByLeague[league]:
          if(isD1(game["awayTeam"],game["homeTeam"],game['m_w'])):
            scoreboard += "{}|{}|{}|{}|{}|{}|\n".format(getFlair(game["awayTeam"]), game["awayScore"], getFlair(game["homeTeam"]), game["homeScore"], game['status'],game['tv'])        
            numGames += 1
    if(numGames == 0):
        scoreboard=scoreboard.replace("#Women's Scores\n","")

    return scoreboard
    
if __name__ == '__main__':
    #global gameDate
    scoreboard=generateScoreboard()
    #getScores()
    print(scoreboard)
