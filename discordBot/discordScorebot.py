import scorebot
import discord
import os
import concurrent.futures as cf
import asyncio,multiprocessing,math
from html.parser import HTMLParser
import urllib.request, urllib.error, urllib.parse
import pytz
import re
import datetime
from time import strftime,localtime
import random
from bs4 import BeautifulSoup
import operator
import itertools
import json
from winprobdata import *
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
season = '1920'
invalidRoles = ['@everyone', 'Mods', 'Admin', 'bot witch', 'Dyno', 'CH_Scorebot']
flairlist = {"St. Cloud State": "<:stcloud:410963404166135809>",
"Minnesota Duluth" : "<:umd:416037206801514496>",
"Minnesota State" : "<:minnstate:502254436694097930>",
"Massachusetts" : "<:umass:509877606628196362>",
"Clarkson" : "<:clarkson:509874830208925706>",
"Northeastern" : "<:northeastern:509874830183628831>",
"Denver" : "<:denver:410963404149358603>",
"Quinnipiac" : "<:quinnipiac:515202909604937748>",
"Ohio State" : "<:ohiostate:410963403952226305>",
"Notre Dame" : "<:notredame:559234890311270453>",
"Cornell" : "<:cornell:509874829927645215>",
"Arizona State" : "<:asu:543115914082516992>",
"Harvard" : "<:harvard:559234780118515712>",
"Providence" : "<:providence:559234548093812736>",
"Bowling Green" : "<:bgsu:559234454120431626>",
"American International" : "<:mrbee:559232704722239489>",
"Wisconsin" : "<:wisconsin:509875125810888705>",
"Minnesota" : "<:minnesota:499717465396477953>"}
flairlist = {}
    #scorebot.getScores()
    #games=scorebot.gameList
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
            data=data.replace(u'\xa0',u' ')
            data=data.lstrip('\n')
            if(data != 'Box' and data != 'Text' and data !=' / ' and data != 'Live - ' and data != '(TV -'):
                
                if(data == 'Sheet'):
                    d += 'Final!'
                elif(data!=' '):
                    d += data + '!'

    def return_data(self):
        global d
        return d

client = discord.Client()
def displayHelp():
    helpStr = '''
?[mscore / wscore] [team name] - current scoreline for Current Men's/Women's game of team entered
?[mstand / wstand] [conference name] - current standings for conference entered
?[cheer / jeer / boo] [team name] - sends random cheers for / jeers against team entered (Suggestions welcome in #suggestion-box)
?[cheer] - cheers for team of user's flair color
?[pwr / krach] - displays current Top 16 Pairwise Ranking / KRACH
?[pwr / krach] top - displays current Top 4 Pairwise Ranking / KRACH
?[pwr / krach] bottom - displays current Bottom 5 Pairwise Ranking / KRACH
?[pwr / krach] bubble - displays the Pairwise Ranking Bubble / KRACH
?[pwr / krach] <number> - displays Top <number\> Pairwise Ranking / KRACH
?[wpwr] - displays current Top 8 Pairwise Ranking
?[wpwr] top - displays current Top 4 Pairwise Ranking
?[wpwr] bottom - displays current Bottom 5 Pairwise Ranking
?[wpwr] bubble - displays the Pairwise Ranking Bubble
?[wpwr] <number> - displays Top <number> Pairwise Ranking
?[wpwr] [team name] - displays Pairwise Ranking of team entered plus 2 teams above and 2 teams below
?[pwc] [team1],[team2] - display Pairwise Comparison between two teams
?[odds] [team1],[team2] - displays KRACH computed odds of winning the matchup
?[odds3] [team1],[team2] - displays KRACH computed odds of winning best of three matchup
?[msched / wsched] [team name] - displays next N games of the team entered
?[mres / wres / mform / wform] [team name] - displays previous N games of the team entered
?[whatsontv] - displays list of Today's games broadcasted on TV
?[thanksbot] - Thanks Bot
?[roles] - display list of availible roles
?[roles] [role/team name] - adds role to user
?[rroles] [role/team name] - removes role from user
?[dog] - displays random dog pic
?[cat] - displays random cat pic

Scores/Standings/TV Listings courtesy of collegehockeystats.net
Pairwise Rankings courtesy of collegehockeynews.com
Women's Pairwise Rankings calculated using scores from collegehockeystats.net
Cheers/Jeers courtesy of Student Sections across America
Bot courtesy of redsoxfan2194
    '''
    return helpStr
def convertTeamtoDisRole(team):
    teams = {   "Air Force" : "Air Force Falcons",
                "Alabama Huntsville" : "Alabama Huntsville Chargers",
                "Alaska" : "Alaska Nanooks",
                "Alaska Anchorage" : "Alaska-Anchorage Seawolves",
                "American International" : "American International Yellow Jackets",
                "Arizona State" : "Arizona State Sun Devils",
                "Army West Point" : "Army Black Knights",
                "Bemidji State" : "Bemidji State Beavers",
                "Bentley" : "Bentley Falcons",
                "Boston College" : "Boston College Eagles",
                "Boston University" : "Boston University Terriers",
                "Bowling Green" : "Bowling Green Falcons",
                "Brown" : "Brown Bears",
                "Canisius" : "Canisius Golden Griffins",
                "Clarkson" : "Clarkson Golden Knights",
                "Colgate" : "Colgate Raiders",
                "Colorado College" : "Colorado College Tigers",
                "Cornell" : "Cornell Big Red",
                "Dartmouth" : "Dartmouth Big Green",
                "Denver" : "Denver Pioneers",
                "Ferris State" : "Ferris State Bulldogs",
                "Franklin Pierce" : "Franklin Pierce Ravens",
                "Georgia Tech" : "Georgia Tech Yellow Jackets",
                "Harvard" : "Harvard Crimson",
                "Holy Cross" : "Holy Cross Crusaders",
                "Lake Superior State" : "Lake Superior State Lakers",
                "Lindenwood" : "Lindenwood Lions",
                "Long Island University" : "LIU Sharks",
                "Maine" : "Maine Black Bears",
                "Mercyhurst" : "Mercyhurst Lakers",
                "Merrimack" : "Merrimack Warriors",
                "Miami" : "Miami RedHawks",
                "Michigan State" : "Michigan State Spartans",
                "Michigan Tech" : "Michigan Tech Huskies",
                "Michigan" : "Michigan Wolverines",
                "Minnesota Duluth" : "Minnesota Duluth Bulldogs",
                "Minnesota" : "Minnesota Golden Gophers",
                "Minnesota State" : "Minnesota State Mavericks",
                "New Hampshire" : "New Hampshire Wildcats",
                "Niagara" : "Niagara Purple Eagles",
                "North Dakota" : "North Dakota Fighting Hawks",
                "Northeastern" : "Northeastern Huskies",
                "Northern Michigan" : "Northern Michigan Wildcats",
                "Notre Dame" : "Notre Dame Fighting Irish",
                "Ohio State" : "Ohio State Buckeyes",
                "Omaha" : "Omaha Mavericks",
                "Penn State" : "Penn State Nittany Lions",
                "Post" : "Post Eagles",
                "Princeton" : "Princeton Tigers",
                "Providence" : "Providence Friars",
                "Quinnipiac" : "Quinnipiac Bobcats",
                "RIT" : "RIT Tigers",
                "Rensselaer" : "RPI Engineers",
                "Robert Morris" : "Robert Morris Colonials",
                "Sacred Heart" : "Sacred Heart Pioneers",
                "Sieve" : "Sieve",
                "St. Anselm" : "St. Anselm Hawks",
                "St. Cloud State" : "St. Cloud State Huskies",
                "St. Lawrence" : "St. Lawrence Saints",
                "St. Michael's" : "St. Michael's Purple Knights",
                "Syracuse" : "Syracuse Orange",
                "UConn" : "UConn Huskies",
                "UMass Lowell" : "UMass Lowell River Hawks",
                "Massachusetts" : "UMass Minutemen",
                "Union" : "Union Dutchmen/Dutchwomen",
                "Vermont" : "Vermont Catamounts",
                "Western Michigan" : "Western Michigan Broncos",
                "Wisconsin" : "Wisconsin Badgers",
                "Yale" : "Yale Bulldogs",
                "UL Lafayette" : "Louisiana Ragin' Cajuns",
                "LSU" : "Louisiana State University Tigers",
                "Georgia Tech" : "Georgia Tech Yellow Jackets",
                "Ref" : "Ref",
                "Meteor" : "Meteor",
                "Portal" : "Portal",
                "Red Sox" : "Red Sox",
                "Yankees" : "Yankees",
                "Jackbox" : "Jackbox Game Night",
                "USA" : "USA",
                "Chaos" : "TEAM CHAOS"}
    if team in teams:
        return teams[team]
    else:
        return ""
def getCheer(role):
    if(role == "color cornell"):
        role = "Cornell Big Red"
    elif(role == "color maine"):
        role = "Maine Black Bears"
    elif(role == "color princeton"):
        role = "Princeton Tigers"
    elif(role == "color vermont"):
        role = "Vermont Catamounts"
    elif(role == "color maine"):
        role = "Maine Black Bears"
    cheerList = { "Boston University Terriers" : ["Go BU!", "Let's Go Terriers!", "BC Sucks!"],
    "Northeastern Huskies" : ["Go NU!", "#HowlinHuskies", "Go Huskies!"],
    "Cornell Big Red" : ["Let's Go Red!", "Go Big Red!", "Fuck Harvard!", "Screw BU!"],
    "Harvard Crimson" : ["Go Harvard!", "Fuck Harvard!"],
    "New Hampshire Wildcats" : ["I Believe in UNH!","Go Wildcats!"],
    "Boston College Eagles" : ["Go BC!", "BC Sucks!", "Go Eagles!", "Sucks to BU!"],
    "UMass Minutemen" : ["Go Amherst!", "Go U Mass!"],
    "UConn Huskies" : ["Go Huskies!", "U-C-O-N-N UCONN UCONN UCONN", "Ice Bus"],
    "Michigan Tech Huskies" : ["Go Huskies!"],
    "UMass Lowell River Hawks" : ["Go River Hawks!"],
    "Clarkson Golden Knights" : ["Let's Go Tech!"],
    "Vermont Catamounts" : ["Go Catamounts!"],
    "Penn State Nittany Lions" : ["We Are!", "Hockey Valley! Clap clap clapclapclap"],
    "Minnesota Golden Gophers" : ["Go Gophers!"],
    "Michigan Wolverines": ["Go Blue!"],
    "Michigan State Spartans" : ["Go Sparty!", "Go Green!"],
    "Sieve": ["Sieve, You Suck!", "Sieve! Sieve! Sieve! Sieve!", "It's All Your Fault!"],
    "RPI Engineers" : ["Let's Go Red!", "Go Red!\nGo White!"],
    "Notre Dame Fighting Irish" : ["Go Irish!"],
    "Providence Friars" : ["Go Friars!"],
    "St. Cloud State Huskies" : ["Go Huskies!"],
    "Minnesota State Mavericks" : ["Go Mavericks!"],
    "Minnesota Duluth Bulldogs" : ["Go Bulldogs!"],
    "Quinnipiac Bobcats" : ["Go Bobcats!", "Meowwww", "Feed. The. Kitty."],
    "Denver Pioneers" : ["Let's Go DU!", "Go Pios!"],
    "Ohio State Buckeyes" : ["Go Buckeyes!"],
    "Arizona State Sun Devils" : ["Forks Up!","Go Sparky!"],
    "Bowling Green Falcons" : ["Ay Ziggy", "Go Ziggy!"],
    "Brown Bears" : ["Go Bruno!"],
    "Yale Bulldogs" : ["Boola Boola"],
    "Wisconsin Badgers" : ["On Wisconsin!"],
    "Merrimack Warriors" : ["Macktion!", "Go Warriors!", "Go Mack!"],
    "Colgate Raiders" : ["Go Gate!"],
    "Colorado College Tigers" : ["Go Tigers! DU still sucks!"],
    "Holy Cross Crusaders" : ["Go Cross Go"],
    "USA" : ["U! S! A!, U! S! A!"],
    "American International Yellow Jackets" : ["Mr. Fucking Bee", "Get Stung!", "Buzz Buzz"],
    "Meteor" : ["https://media.tenor.com/images/892268e557475c225acebe707c85bffc/tenor.gif"],
    "Red Sox" : ["Go Red Sox!", "Yankees Suck!"],
    "Portal" : ["PRAISE PORTAL"],
    "Louisiana Ragin' Cajuns": ["Geaux Cajuns!"]}
    if role in cheerList:   
            return random.choice(cheerList[role])
    else:
        return "";
        
def getJeer(role):
    if(role == "color cornell"):
        role = "Cornell Big Red"
    elif(role == "color maine"):
        role = "Maine Black Bears"
    elif(role == "color princeton"):
        role = "Princeton Tigers"
    elif(role == "color vermont"):
        role = "Vermont Catamounts"
    jeerList = { "Boston College Eagles" : ["BC Sucks!", "Fuck 'Em Up! Fuck 'Em Up! BC Sucks!", "Sunday School!", "Not From Boston!" ,"```For Newton, For Newton\nThe Outhouse on the hill!\nFor Newton, For Newton\nBC sucks and always will!\nSo here’s to the outhouse on the hill,\nCause Boston College sucks and they always will,\nFor Newton, For Newton,\nThe outhouse on the hill!```"],
    "Harvard Crimson" : ["Fuck Harvard!", "Gimme an A! Gimme another A! Gimme another A! Grade Inflation!", "UMass Rejects!"],
    "Yale Bulldogs" : ["Yuck Fale", "UConn Rejects!", "I wouldn't jeer me if i were you. Do you know who my father is?"],
    "Dartmouth Big Green" : ["UNH Rejects!"],
    "Union Dutchmen/Dutchwomen" : ["Can't spell sucks without UC!!"],
    "Brown Bears" : ["URI Rejects!", "Brown is Shit! Shit is Brown!", "Around the bowl, down the hole, flush, flush, flush", "if it's brown, flush it down!"],
    "Princeton Tigers" : ["Rutgers Rejects!", "Princeton's in New Jerseyyy"],
    "Providence Friars" : ["https://widget.campusexplorer.com/media/original/media-7CA07320.jpg"],
    "UMass Lowell River Hawks" : ["What's a River Hawk?","Low\nLower\nLowest\nLowell"],
    "UMass Minutemen" : ["Please Don't Riot!", "We Last Longer!","Think of those couches...they have family", "Embarrassment of the Commonwealth", "https://i.imgur.com/u1SCJ73.gifv"],
    "Boston University Terriers" : ["Sucks to BU!", "Screw BU!"],
    "Northeastern Huskies" : ["Northleastern", "North! Eastern! Sucks!"],
    "Colgate Raiders" : ["Crest is Best!"],
    "Cornell Big Red" : ["Harvard Rejects!", "```Up above Cayuga's waters, there's an awful smell;\nThirty thousand Harvard rejects call themselves Cornell.\nFlush the toilet, flush the toilet,\nFlush them all to hell!\nThirty thousand Harvard rejects call themselves Cornell!```"],
    "Maine Black Bears" : ["M-A-I-N-E ~~Go Blue~~ MAAAAAIIINNNE SUCKS"],
    "Louisiana State University Tigers" :["Louisiana State University and Agricultural and Mechanical College"],
    "Wisconsin Badgers" : ["Dirty Sconnies", "https://i.imgur.com/sljug4m.jpg"],
    "Michigan State Spartans" : ["Poor Sparty"],
    "Notre Dame Fighting Irish" : ["Blinded by the Light", "Notre Lame!", "Rudy was offsides!"],
    "St. Cloud State Huskies" : ["Go back to Montreal!", "St. Cloud Sucks!", "St. Cloud is not a state"],
    "RPI Engineers" : ["KRACH is Better!"],
    "Minnesota State Mavericks" : ["Mankatno", "Mankato Sucks!"],
    "Minnesota Duluth Bulldogs" : ["Duluth Sucks!"],
    "Quinnipiac Bobcats" : ["QU PU!"],
    "Michigan Tech Huskies" : ["Even Mel had to leave Houghton."],
    "Denver Pioneers" : ["Sucks to DU!"],
    "Ohio State Buckeyes" : ["An Ohio State University"],
    "Arizona State Sun Devils" : ["Forked", "Fork You!", "Poor Sparky"],
    "Bowling Green Falcons" : ["Boo Ziggy"],
    "American International Yellow Jackets" : ["NO ONE JEERS MR. FUCKING. BEE."],
    "Clarkson Golden Knights" : ["It's " + strftime("%H:%M", localtime()) + " and Clarkson still sucks!"],
    "Vermont Catamounts" : ["Elephants Don't Walk That Way", "Dirty Hippies"],
    "UConn Huskies" : ["Slush Bus", "U-Cons"],
    "New Hampshire Wildcats" : ["Bad Kitty"],
    "Holy Cross Crusaders" : ["Boo Cross Boo", "Holy Cow"],
    "Sieve": ["Sieve, You Suck!", "Sieve! Sieve! Sieve! Sieve!", "It's All Your Fault!"],
    "Yankees" : ["Yankees Suck!"],
    "Ref": ["I'm Blind! I'm Deaf! I wanna be a ref!", "Hey Ref, check your phone, you missed a few calls.", "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", ":regional_indicator_b: :regional_indicator_u: :regional_indicator_l: :regional_indicator_l: :regional_indicator_s: :regional_indicator_h: :regional_indicator_i: :regional_indicator_t:"]}
    if role in jeerList:
            return random.choice(jeerList[role])
    else:
        return "";
 
def getPairwise(opt):
    url = "https://www.collegehockeynews.com/ratings/m/pairwise.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    data =soup.get_text()
    pairwise = []
    for link in soup.find_all('a'):
        if("\n" not in link.get_text() and '' != link.get_text() and 'Customizer' != link.get_text() and 'Primer' != link.get_text() and 'Glossary' != link.get_text()):
            pairwise.append(link.get_text())       

    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
    teams = []
    start = 0
    decodedTeam = decodeTeam(opt)
    if(opt.isnumeric()):
        end = int(opt)
    elif(opt.lower()=='full'):
        end = 60
    elif(scorebot.isD1(decodedTeam,decodedTeam,'Men') or decodedTeam in chnDiffs.keys()):
        if(decodedTeam in chnDiffs.keys()):        
            teamIdx=pairwise.index(chnDiffs[decodedTeam])
        else:
            teamIdx=pairwise.index(decodedTeam)
        if(teamIdx-2<0):
            start=0
        else:
            start = teamIdx-2
        if(teamIdx+3>60):
            end=60
        else:
            end = teamIdx+3
    elif(opt.lower() == 'bubble'):
        start = 12
        end = 20
    elif(opt.lower() == 'top'):
        end = 4
    elif(opt.lower() == 'bottom'):
        start = 55
        end = 60
    else:
        end = 16

    rankings = "```"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,pairwise[i])
    rankings += "```"
    return rankings
def getKRACH(opt):
    url = "https://www.collegehockeynews.com/ratings/krach.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    krach = []
    for i in soup.findChildren('tr'):
        cells = i.findChildren('td')
        line = ""
        for cell in cells:
         value = cell.string
         if(value != None):
            line +=value + "!"
        if(line and 'RRWP' not in line and 'Ratio' not in line and 'Strength' not in line):
            line=line.rstrip('!')
            krach.append(line.split("!")[1])       

    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
    teams = []
    start = 0
    decodedTeam = decodeTeam(opt)
    if(opt.isnumeric()):
        end = int(opt)
    elif(opt.lower()=='full'):
        end = 60
    elif(scorebot.isD1(decodedTeam,decodedTeam,'Men') or decodedTeam in chnDiffs.keys()):
        if(decodedTeam in chnDiffs.keys()):        
            teamIdx=krach.index(chnDiffs[decodedTeam])
        else:
            teamIdx=krach.index(decodedTeam)
        if(teamIdx-2<0):
            start=0
        else:
            start = teamIdx-2
        if(teamIdx+3>60):
            end=60
        else:
            end = teamIdx+3
    elif(opt.lower() == 'bubble'):
        start = 12
        end = 20
    elif(opt.lower() == 'top'):
        end = 4
    elif(opt.lower() == 'bottom'):
        start = 55
        end = 60
    else:
        end = 16

    rankings = "```"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,krach[i])
    rankings += "```"
    return rankings
    
def getWinProb(aTeam, aScore, hTeam, hScore, status):
    if('Final' in status):
        return ''
      
    return ''
    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
        
    hTeam = decodeTeam(hTeam)
    aTeam = decodeTeam(aTeam)
    origHTeam = hTeam
    origATeam = aTeam
    if(scorebot.isD1(hTeam,hTeam,'Men') or hTeam in chnDiffs.keys()):
        if(hTeam in chnDiffs.keys()): 
            origHTeam = hTeam
            hTeam=chnDiffs[hTeam]
            
    
    if(scorebot.isD1(aTeam,aTeam,'Men') or aTeam in chnDiffs.keys()):
        if(aTeam in chnDiffs.keys()):
            origATeam = aTeam        
            aTeam=chnDiffs[aTeam]
    krach = {}       
    url = "https://www.collegehockeynews.com/ratings/krach.php"
    url = "https://www.collegehockeynews.com/ratings/krach/2019" #TODO Remove when KRACH works
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    krach = {}
    for i in soup.findChildren('tr'):
        cells = i.findChildren('td')
        line = ""
        for cell in cells:
         value = cell.string
         if(value != None):
            line +=value + "!"
        if(line and 'RRWP' not in line and 'Ratio' not in line and 'Strength' not in line):
            line=line.rstrip('!')
            line=line.split("!")
            krach[line[1]]=float(line[2])
      
    if(hTeam in krach.keys() and aTeam in krach.keys()):
        hOdds = krach[hTeam]/(krach[hTeam]+krach[aTeam])
        aOdds = krach[aTeam]/(krach[hTeam]+krach[aTeam])
    else:
        aOdds=.5
        hOdds=.5
    
    if(aTeam != origATeam):
        aTeam = origATeam
        
    if(hTeam != origHTeam):
        hTeam = origHTeam
        
    if('am' in status or 'pm' in status):
        if(hOdds>aOdds):
            return "{} {}%".format(hTeam,round((hOdds)*100,1))
        elif(aOdds>hOdds):
            return "{} {}%".format(aTeam,round((aOdds)*100,1))
        else:
            return "Even"
    time,per = status.split('  ')
    secTime=0
    if(time != 'End'):
        if(time != 'Start'):
            secTime=time.split(':')
            secTime=int(secTime[0])*60+math.ceil(float(secTime[1]))
            secTime = 1200 - secTime
        if(per == '2nd'):
            secTime += 1200
        elif(per == '3rd'):
            secTime += 2400
        elif(per == 'OT'):
            secTime += 3600
    elif(time == 'End'):
        if(per == '2nd'):
            secTime = 2400
        elif(per == '3rd'):
            secTime = 3600
        elif(per == 'OT'):
            return ''
            
    secTime -= secTime % 5 
    hOdds -= .5
    aOdds -= .5
    gd=abs(int(hScore)-int(aScore))
    if(gd>6):
        gd=6
    if(gd==0):
        tiedProb = float(tiedLookup[str(secTime)][0])
        if(hOdds>aOdds):
            return "{} {}%".format(hTeam,round((hOdds+.5)*100,1))
        elif(aOdds>hOdds):
            return "{} {}%".format(aTeam,round((aOdds+.5)*100,1))
        else:
            return "Even"
    
    if(hScore>aScore):
        winProb = float(winLookup[str(secTime)][gd])
        return "{} {}%".format(hTeam,round(hOdds*(1-secTime/3600)+winProb*100,1))
    
    if(aScore>hScore):
        winProb = float(winLookup[str(secTime)][gd])
        return "{} {}%".format(aTeam,round(aOdds*(1-secTime/3600)+winProb*100,1))
    
def getKOdds(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
    
    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
        
    team1 = decodeTeam(team1)
    team2 = decodeTeam(team2)
    if(scorebot.isD1(team1,team1,'Men') or team1 in chnDiffs.keys()):
        if(team1 in chnDiffs.keys()):       
            team1=chnDiffs[team1]
    else:
        return "Team 1 Not Found"
    
    if(scorebot.isD1(team2,team2,'Men') or team2 in chnDiffs.keys()):
        if(team2 in chnDiffs.keys()):       
            team2=chnDiffs[team2]
    else:
        return "Team 2 Not Found"
    url = "https://www.collegehockeynews.com/ratings/krach.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    krach = {}
    for i in soup.findChildren('tr'):
        cells = i.findChildren('td')
        line = ""
        for cell in cells:
         value = cell.string
         if(value != None):
            line +=value + "!"
        if(line and 'RRWP' not in line and 'Ratio' not in line and 'Strength' not in line):
            line=line.rstrip('!')
            line=line.split("!")
            krach[line[1]]=float(line[2])
    
    team1Odds = krach[team1]/(krach[team1]+krach[team2])
    team2Odds = krach[team2]/(krach[team1]+krach[team2])
    
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))

def getKOdds3(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
    
    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
        
    team1 = decodeTeam(team1)
    team2 = decodeTeam(team2)
    if(scorebot.isD1(team1,team1,'Men') or team1 in chnDiffs.keys()):
        if(team1 in chnDiffs.keys()):       
            team1=chnDiffs[team1]
    else:
        return "Team 1 Not Found"
    
    if(scorebot.isD1(team2,team2,'Men') or team2 in chnDiffs.keys()):
        if(team2 in chnDiffs.keys()):       
            team2=chnDiffs[team2]
    else:
        return "Team 2 Not Found"
    url = "https://www.collegehockeynews.com/ratings/krach.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    krach = {}
    for i in soup.findChildren('tr'):
        cells = i.findChildren('td')
        line = ""
        for cell in cells:
         value = cell.string
         if(value != None):
            line +=value + "!"
        if(line and 'RRWP' not in line and 'Ratio' not in line and 'Strength' not in line):
            line=line.rstrip('!')
            line=line.split("!")
            krach[line[1]]=float(line[2])
    
    team1Odds = (krach[team1]**2 * (krach[team1] + 3 * krach[team2]))/((krach[team1] + krach[team2])**3)
    team2Odds = (krach[team2]**2 * (krach[team2] + 3 * krach[team1]))/((krach[team2] + krach[team1])**3)
    
    
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))

def getPWRComp(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
        
    chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
        "Lake Superior State" : "Lake Superior",
        "UMass Lowell" : "Mass.-Lowell",
        "Omaha" : "Nebraska-Omaha",
        "American International" : "American Int'l",
        "Army West Point" : "Army",
        "Alabama Huntsville" : "Alabama-Huntsville",
        "Alaska Anchorage" : "Alaska-Anchorage",
        "UConn" : "Connecticut"}
        
    team1 = decodeTeam(team1)
    team2 = decodeTeam(team2)
    if(scorebot.isD1(team1,team1,'Men') or team1 in chnDiffs.keys()):
        if(team1 in chnDiffs.keys()):       
            team1=chnDiffs[team1]
    else:
        return "Team 1 Not Found"
    
    if(scorebot.isD1(team2,team2,'Men') or team2 in chnDiffs.keys()):
        if(team2 in chnDiffs.keys()):       
            team2=chnDiffs[team2]
    else:
        return "Team 2 Not Found"
    if(team1 == team2):
        return "Enter Two Different Teams!"
    url = "https://www.collegehockeynews.com/ratings/m/pairwise.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    pairwise = []
    hrefDict = {}
    for link in soup.find_all('a'):
        if("\n" not in link.get_text() and '' != link.get_text() and 'Customizer' != link.get_text() and 'Primer' != link.get_text() and 'Glossary' != link.get_text()):
            idNum=re.search('.*=(.*)',link['href'])
            idNum=idNum.group(1)
            hrefDict[link.get_text()]=[idNum,[]]

    url = "https://www.collegehockeynews.com/ratings/m/comparison.php?td={}&od={}".format(hrefDict[team1][0],hrefDict[team2][0])
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    compList=[]
    for i in soup.find_all('tr'):
        line = ''
        for d in i.find_all('td'):
            d=d.get_text()
            d=d.replace(u'\u2011',u'-')
            d=d.replace(u'\xa0',u'')
            line+=d + "!"
        if(line != '' and line != team1):
            comp=line.split("!")
            comp.pop()
            if(len(comp)==5):
                compList.append(comp)
            
        if(i.find('th')):
            if(i.find('th').get_text()!=team1 and i.find('th').get_text()!=""):
                comp.insert(3,i.find('th').get_text())
                if('H2H' in comp):
                    temp=comp[0]
                    comp[1]=temp
                    comp[0]=''
                    temp=comp[-1]
                    comp[-2]=temp
                    comp[-1]=''
                compList.append(comp)
    pwrComp = '```'
    for i in compList:
        for d in i:
            pwrComp+= d + '\t'
        pwrComp += '\n'
    pwrComp+='```'
    return pwrComp
def getStandings(conf, m_w):
    global season
    conf=conf.lower()
    conf=conf.replace(" ","")
    if(m_w == "Men"):
        if(conf=="hea" or conf == "he" or conf == 'hockeyeast'):
            conference = "heastm"
        elif(conf == "ivy"):
            conference = "ivym"
        elif(conf == "atlantic" or conf == "ahc" or conf == "aha"):
            conference = "atlantic"
        elif(conf == "bigten" or conf == "b10" or conf == "b1g" or conf == "big10" ):
            conference = "bigten"
        elif(conf == "nchc"):
            conference = "nchc"
        elif(conf == "wcha"):
            conference = "wcham"
        elif(conf == "ecac"):
            conference = "ecachm"
        elif(conf == "ind" or conf == "independent"):
            conference = "indm1"
        else:
            return "I don't know that conference."
    elif(m_w == "Women"):
        if(conf=="hea" or conf == "he" or conf == 'hockeyeast'):
            conference = "heastw"
        elif(conf == "ivy"):
            conference = "ivyw"
        elif(conf == "cha"):
            conference = "chaw"
        elif(conf == "wcha"):
            conference = "wchaw"
        elif(conf == "ecac"):
            conference = "ecachw"
        elif(conf == "newha"):
            conference = "newha"
        else:
            return "I don't know that conference."
    else:
        return "I don't know that conference."

    url = "http://www.collegehockeystats.net/{}/standings/{}".format(season,conference)
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    data =soup.get_text()
    for i in soup.find_all('pre'):
        data=i.get_text()
        standings=data.replace(u'\xa0',u' ') 
        standings = "```" + standings + "```"
        return standings
        
def getGamesOnTV():
    parser = MyHTMLParser()
    url = "http://collegehockeystats.net/"
    f=urllib.request.urlopen(url,timeout=10)
    html = f.read()
    f.close()
    parser.feed(html.decode("ISO-8859-1"))
    
    if("<meta HTTP-EQUIV=\"REFRESH\"" in html.decode("ISO-8859-1")):
        html = html.decode("ISO-8859-1")
        url=html.split("url=")
        url=url[1].split("\"")[0]
        f=urllib.request.urlopen(url,timeout = 10)
        html = f.read()
        f.close()
        parser.feed(html.decode("ISO-8859-1"))
    gameData=parser.return_data()

    days = gameData.split('\n\n')
    games = days[0].split('\n')
    #print(games)    
    mtagLookup = {}
    wtagLookup = {}
    leagues=set()
    gameList = []
    tag = ''
    for game in games:
        #print(game)
        game = game.split('!')
        channel = ''
        if any("TV" in i for i in game):
            channel=[i for i in game if "TV" in i][0].lstrip(' ')
            channel=channel.replace("(TV-","")
            channel=channel.replace(")","")
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
            if(game[0]==''):
                continue            
            if(game[0][0]=='('):
                tag=game[0]
                game.pop(0)                
        if(game.count('OT')>0):
            numOT = 'OT'
            if(game.count('2OT')>0):
                numOT = '2OT'
            elif(game.count('3OT')>0):
                numOT = '3OT'
            elif(game.count('4OT')>0):
                numOT = '4OT'
            game.pop(5)
            if(game.count('Final')>0):
                game[7]='Final ({})'.format(numOT)
        if(len(game)==8):
            game[5]=game[5].replace(' ',"")
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
                        'm_w': m_w,
                        'channel' : channel}
            leagues.add(game[5])
            gameList.append(gameDict)
        if(len(game)==9):
          game[5]=game[5].replace(' ',"")
          if(game[5]=='EC,IV'):
            game[5] = 'EC'
          if(m_w == 'Women' and game[5]=='NH'):
              game[5] = 'NW'
          if(tag):
            if(m_w=='Men' and tag in list(mtagLookup.keys())):
              game[5]=mtagLookup[tag]
            if(m_w=='Women' and tag in list(wtagLookup.keys())):
               game[5]=wtagLookup[tag]
          time = game[8] + ' ' + game[7]
          gameDict = {  'awayTeam' : game[0],
                        'awayScore': game[1],
                        'homeTeam' : game[3],
                        'homeScore': game[4],
                        'league' : game[5],
                        'startTime': game[6],
                        'status' : time,
                        'm_w' : m_w,
                        'channel' : channel}
          leagues.add(game[5])
          gameList.append(gameDict)
        if(len(game)==5):
            game[3]=game[3].replace(' ',"")
            if(game[3]=='EC,IV'):
              game[3] = 'EC'
            if(m_w == 'Women' and game[3]=='NH'):
              game[3] = 'NW'
            gameDict = {'awayTeam' : game[0],
                        'awayScore': "",
                        'homeTeam' : game[2],
                        'homeScore': "",
                        'league' : game[3],
                        'startTime': game[4],
                        'status' : game[4],
                        'm_w': m_w,
                        'channel' : channel}
            leagues.add(game[3])
            gameList.append(gameDict)
    tvGames = ""
    for game in gameList:
        if(game['channel'] != ''):
            if("am" not in game['status'] and "pm" not in game['status']):
                if('Final' in game['status']):
                    game['startTime'] = 'Ended'
                else:
                    game['startTime'] = 'On Now'
                
            tvGames += game['m_w'] + ": " + game['awayTeam'] + " @ " + game['homeTeam'] + " - " + game['startTime'] + " (" + game['channel'] + ')\n'
    return tvGames
def calcUWP():
    global teamDict
    for i in teamDict.keys():
       teamDict[i]['WP'] = (len(teamDict[i]['Wins'])+(len(teamDict[i]['Ties'])*.5))/teamDict[i]['GP']
       
def calcUoWP():
    global teamDict
    for i in teamDict.keys():
        for d in teamDict[i]['teamsPlayed']:
            if((teamDict[d]['GP']-teamDict[d]['teamsPlayed'].count(i))>0):
                teamDict[i]['oWP']+=((len(teamDict[d]['Wins'])-teamDict[d]['Wins'].count(i))+((len(teamDict[d]['Ties'])-teamDict[d]['Ties'].count(i))*.5))/(teamDict[d]['GP']-teamDict[d]['teamsPlayed'].count(i))
            
        teamDict[i]['oWP'] /= len(teamDict[i]['teamsPlayed'])
    
def calcooWP():
    global teamDict
    for i in teamDict.keys():
        for d in teamDict[i]['teamsPlayed']:
            teamDict[i]['ooWP']+=teamDict[d]['oWP']
        teamDict[i]['ooWP']/=len(teamDict[i]['teamsPlayed'])

def calcURPI():
    global teamDict
    calcUWP()
    calcUoWP()
    calcooWP()
    for i in teamDict.keys():
        teamDict[i]['uRPI']=teamDict[i]['WP']*.3 + teamDict[i]['oWP']*.24 + teamDict[i]['ooWP']*.46
        
def calcQWB():
    global teamDict,newha
    rpiDict = {}
    for i in teamDict.keys():
        if(i not in newha):
            rpiDict[i] = teamDict[i]['uRPI']
            
    sorted_rpi = sorted(rpiDict.items(), key=operator.itemgetter(1),reverse=True)
    bonus=0.06
    qwbDict={}
    for i in sorted_rpi:

        if(bonus<=0):
            bonus=0
        qwbDict[i[0]]=round(bonus,4)
        bonus-=.005
    for i in teamDict.keys():
        for d in teamDict[i]['Wins']:
            if(d in qwbDict.keys()):
                teamDict[i]['QWB'] += qwbDict[d]
                
        for d in teamDict[i]['Ties']:
            if(d in qwbDict.keys()):
                teamDict[i]['QWB'] += qwbDict[d]*.5
      
        teamDict[i]['QWB']/= teamDict[i]['GP']   
def calcRPI():
    global teamDict
    calcURPI()
    removeBadWins()
    calcQWB()
    for i in teamDict.keys():
        if(i not in newha):
            teamDict[i]['RPI']=teamDict[i]['uRPI'] + teamDict[i]['QWB']
def removeBadWins():
    global teamDict
    for i in  teamDict.keys():
        WP = 0
        removeCount = 0
        removeRPI = 0
        for d in teamDict[i]['Wins']:
            if((teamDict[d]['GP']-teamDict[d]['teamsPlayed'].count(i))>0):
                WP = ((len(teamDict[d]['Wins'])-teamDict[d]['Wins'].count(i))+((len(teamDict[d]['Ties'])-teamDict[d]['Ties'].count(i))*.5))/(teamDict[d]['GP']-teamDict[d]['teamsPlayed'].count(i))
                
            gameRPI = .30+ WP*.24 + teamDict[d]['oWP']*.46
            if(gameRPI+0.000001<teamDict[i]['uRPI']):
                removeRPI += gameRPI
                removeCount += 1
        
        teamDict[i]['uRPI'] = (teamDict[i]['uRPI'] * teamDict[i]['GP'] - removeRPI)/(teamDict[i]['GP']-removeCount)
def compareRPI(team1, team2):
    global teamDict
    if(teamDict[team1]['RPI']>teamDict[team2]['RPI']):
        return [1,0]
    elif(teamDict[team1]['RPI']<teamDict[team2]['RPI']):
        return [0,1]
    else:
        return [0,0]
def compareCoOpp(team1,team2):
    global teamDict
    coOpp = set(teamDict[team1]['teamsPlayed']) - (set(teamDict[team1]['teamsPlayed']) - set(teamDict[team2]['teamsPlayed']))
    t1Copp = 0
    t2Copp = 0
    for i in coOpp:
        t1Copp += (teamDict[team1]['Wins'].count(i) + teamDict[team1]['Ties'].count(i)*.5) / (teamDict[team1]['Wins'].count(i) + teamDict[team1]['Ties'].count(i) + teamDict[team1]['Losses'].count(i))
        t2Copp += (teamDict[team2]['Wins'].count(i) + teamDict[team2]['Ties'].count(i)*.5) / (teamDict[team2]['Wins'].count(i) + teamDict[team2]['Ties'].count(i) + teamDict[team2]['Losses'].count(i))
    if(round(t1Copp,6)>round(t2Copp,6)):
        return [1,0]
    elif(round(t1Copp,6)<round(t2Copp,6)):
        return [0,1]
    else:
        return [0,0]
def compareH2H(team1, team2):
    if team1 in teamDict[team2]['teamsPlayed']:
        return [teamDict[team1]['Wins'].count(team2),teamDict[team2]['Wins'].count(team1)]
    else:
        return [0,0]
        
def compareTeams(team1,team2):
    t1RPI,t2RPI=compareRPI(team1, team2)
    t1CoOpp,t2CoOpp=compareCoOpp(team1,team2)
    t1H2H,t2H2H=compareH2H(team1,team2)
    sumTeam1 = t1RPI + t1CoOpp + t1H2H
    sumTeam2 = t2RPI + t2CoOpp + t2H2H
    return [sumTeam1,sumTeam2]
    
def getWPairwise(opt):
    global teamDict,newha,season
    #newha =['Saint Anselm','Franklin Pierce',"Saint Michael's"]   
    newha = []
    url = "http://www.collegehockeystats.net/{}/schedules/ncw".format(season)
      
    parser = MyHTMLParser()
    f=urllib.request.urlopen(url,timeout=10)
    html = f.read()
    f.close()
    parser.feed(html.decode("latin1"))
    
    gameData=parser.return_data()
    teamDict = {}
    days = gameData.split('\n\n')
    for day in days:
        games = day.split('\n')
        #print(games)    
        mtagLookup = {}
        wtagLookup = {}
        leagues=set()
        gameList = []
        tag = ''
        for game in games:
            #print(game)
            game = game.split('!')
            if(len(game)==1):
                continue
            if(game[0]==''):
                game.pop(0)

            if(game[-1]==''):
                game.pop()
                if(game==[]):
                    continue
                try:
                    if(game[-1][0]=='('):
                        game.pop()
                except IndexError:
                    pass
            if(len(game)==2):
               continue
                   
            if(len(game)>2):
                if(game[0]==''):
                    continue            
                if(game[0][0]=='('):
                    tag=game[0]
                    game.pop(0)                
            if(game.count('OT')>0):
                numOT = 'OT'
                if(game.count('2OT')>0):
                    numOT = '2OT'
                elif(game.count('3OT')>0):
                    numOT = '3OT'
                elif(game.count('4OT')>0):
                    numOT = '4OT'
                game.pop(5)
                if(game.count('Final')>0):
                    game[7]='Final ({})'.format(numOT)
            if(len(game)==8):
                game[5]=game[5].replace(' ',"")
                if(game[5]=='EC,IV'):
                   game[5] = 'EC'
                if(game[5]=='NH'):
                  game[5] = 'NW' 
                game[4] = game[4].replace(' OT','')
                pwrGameDict = {'awayTeam' : game[0],
                            'awayScore': game[1],
                            'homeTeam' : game[3],
                            'homeScore': game[4]}
                if(game[5]=='EX' or not scorebot.isD1(pwrGameDict['homeTeam'],pwrGameDict['homeTeam'],'Women') or not scorebot.isD1(pwrGameDict['awayTeam'],pwrGameDict['awayTeam'],'Women')):
                    continue
                if(pwrGameDict['homeTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['homeTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "oWP": 0, "ooWP": 0, 'teamsPlayed': [], "uRPI" : 0, 'RPI': 0, 'QWB': 0, 'cWins': 0}})
                if(pwrGameDict['awayTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['awayTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "oWP": 0, "ooWP": 0, 'teamsPlayed': [], "uRPI" : 0, 'RPI': 0, 'QWB' : 0, 'cWins': 0}})
                
                if(pwrGameDict['homeScore'] > pwrGameDict['awayScore']):
                    teamDict[pwrGameDict['homeTeam']]['Wins'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Losses'].append(pwrGameDict['homeTeam'])
                    
                elif(pwrGameDict['homeScore'] == pwrGameDict['awayScore']):
                    teamDict[pwrGameDict['homeTeam']]['Ties'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Ties'].append(pwrGameDict['homeTeam'])
                else:
                    teamDict[pwrGameDict['homeTeam']]['Losses'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Wins'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['teamsPlayed'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['teamsPlayed'].append(pwrGameDict['awayTeam'])  


    
    calcRPI()
    teamList = [i for i in teamDict.keys() if scorebot.isD1(i,i,'Women') and i not in newha]

    teamCombos=list(itertools.combinations(teamList,2))
    for team1,team2 in teamCombos:
        sumTeam1,sumTeam2 = compareTeams(team1,team2)
        if(sumTeam1>sumTeam2):
            teamDict[team1]['cWins']+=1
        elif(sumTeam1<sumTeam2):
            teamDict[team2]['cWins']+=1
        else:
            t1RPI,t2RPI = compareRPI(team1,team2)
            if(t1RPI>t2RPI):
                teamDict[team1]['cWins']+=1
            elif(t1RPI<t2RPI):
                teamDict[team2]['cWins']+=1
    pwrDict ={}
    for i in teamDict.keys():
        if(scorebot.isD1(i,i,'Women')):
            pwrDict[i] = [teamDict[i]['cWins'],teamDict[i]['RPI']]
        
    sorted_pwr = sorted(pwrDict.items(), key=operator.itemgetter(1,1), reverse=True)
    pwr = []
    for i in sorted_pwr:
        pwr.append(i[0])
    start = 0
    decodedTeam = decodeTeam(opt)
    if(opt.isnumeric()):
        end = int(opt)
    elif(opt.lower()=='full'):
        end = 40
    elif(scorebot.isD1(decodedTeam,decodedTeam,'Women')):

        teamIdx=pwr.index(decodedTeam)
        if(teamIdx-2<0):
            start=0
        else:
            start = teamIdx-2
        if(teamIdx+3>40):
            end=40
        else:
            end = teamIdx+3
    elif(opt.lower() == 'bubble'):
        start = 5
        end = 12
    elif(opt.lower() == 'top'):
        end = 4
    elif(opt.lower() == 'bottom'):
        start = 35
        end = 40
    else:
        end = 8
    rankings = "```"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,pwr[i])
    rankings += "```"
    return rankings

@client.event
async def on_message(message):
    global invalidRoles
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
       await message.author.send(displayHelp())
    if not message.content.startswith('?'):
        return
    loop = asyncio.get_event_loop()
    if message.content.startswith('?score '):
        team = decodeTeam(message.content.split('?score ')[1])
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generateScoreline, team, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?mscore '):
        team = decodeTeam(message.content.split('?mscore ')[1])
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generateScoreline, team, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
       
            
    if message.content.startswith('?wscore '):
        team = decodeTeam(message.content.split('?wscore ')[1])
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generateScoreline, team, "Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
            
    if message.content.startswith('?msched '):
        team = decodeTeam(message.content.split('?msched ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?sched '):
        team = decodeTeam(message.content.split('?sched ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wsched '):
        team = decodeTeam(message.content.split('?wsched ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
          
    if message.content.startswith('?mres '):
        team = decodeTeam(message.content.split('?mres ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?res '):
        team = decodeTeam(message.content.split('?res ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wres '):
        team = decodeTeam(message.content.split('?wres ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg) 

    if message.content.startswith('?mform '):
        team = decodeTeam(message.content.split('?mform ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?form '):
        team = decodeTeam(message.content.split('?form ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wform '):
        team = decodeTeam(message.content.split('?wform ')[1])
        opt='5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)              
            
    if message.content.startswith('?thanksbot'):
        msg = "You're Welcome {0.author.mention}!".format(message)
        for i in range(len(message.author.roles)):
            if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch"):
                cheer = getCheer(message.author.roles[-1-i].name)
                break
      
        if(cheer!=""):
            msg+="\n{}".format(cheer)
        await message.channel.send(msg)
    
    if message.content.startswith('?cheer'):
        team = message.content.split('?cheer ')
        if(len(team)>1):
            team=decodeTeam(team[1])
        if(len(team)==1):
            for i in range(len(message.author.roles)):
                if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch"):
                    cheer = getCheer(message.author.roles[-1-i].name)
                    break
        else:
            cheer = getCheer(convertTeamtoDisRole(team))
            
        if(cheer!=""):
            msg="{}".format(cheer)
        else:
            msg = "I don't know that cheer."
        await message.channel.send(msg)
        
    if message.content.startswith('?jeer '):
        team = message.content.split('?jeer ')
        jeer = ""
        if(len(team)>1):
            team=decodeTeam(team[1])
            jeer = getJeer(convertTeamtoDisRole(team))
            
        if(jeer!=""):
            msg="{}".format(jeer)
        else:
            msg = "I don't know that jeer."
        await message.channel.send(msg)
    if message.content.startswith('?boo '):
        team = message.content.split('?boo ')
        jeer = ""
        if(len(team)>1):
            team=decodeTeam(team[1])
            jeer = getJeer(convertTeamtoDisRole(team))
            
        if(jeer!=""):
            msg="{}".format(jeer)
        else:
            msg = "I don't know that jeer."
        await message.channel.send(msg)
       
    if(message.content.startswith('?pwr')):
        opt = message.content.split('?pwr ')
        if(len(opt)==1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getPairwise, '')
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getPairwise, opt[1])
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
                
    if(message.content.startswith('?wpwr')):
        opt = message.content.split('?wpwr ')
        if(len(opt)==1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWPairwise, '')
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWPairwise, opt[1])
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg) 
                
    if(message.content.startswith('?krach')):
        opt = message.content.split('?krach ')
        if(len(opt)==1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getKRACH, '')
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getKRACH, opt[1])
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)                
    if(message.content.startswith('?mstand')):
        conf = message.content.split('?mstand ')
        if(len(conf)>1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getStandings, conf[1], "Men")
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
                await message.channel.send("I don't know that conference.")
                
    if(message.content.startswith('?wstand')):
        conf = message.content.split('?wstand ')
        if(len(conf)>1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getStandings, conf[1], "Women")
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
                await message.channel.send("I don't know that conference.")
    if(message.content.startswith('?whatsontv')):
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getGamesOnTV)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
        else:
             await message.channel.send("No Games on TV Today")
    if(message.content.startswith('?odds ')):
        team1= ''
        team2= ''
        teams = message.content.split('?odds ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
                
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getKOdds,  team1, team2)
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
             await message.channel.send("Invalid number of teams, enter two comma separated teams")
    if(message.content.startswith('?odds3 ')):
        team1= ''
        team2= ''
        teams = message.content.split('?odds3 ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
                
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getKOdds3,  team1, team2)
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
             await message.channel.send("Invalid number of teams, enter two comma separated teams")
             
    if(message.content.startswith('?pwc ')):
        team1= ''
        team2= ''
        teams = message.content.split('?pwc ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
                
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getPWRComp,  team1, team2)
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
             await message.channel.send("Invalid number of teams, enter two comma separated teams")   
    
    if(message.content.startswith('?roles')):
        try:
            roleChoice = message.content.split('?roles ')
            if(len(roleChoice)==1):
                    
                roles = "```"
                
                for i in message.guild.roles:
                    if(i.name not in invalidRoles):
                        roles+= i.name + "\n"
                if(roles != "```"):
                    roles += '```'
                    await message.author.send(roles) 
            else:
                team=convertTeamtoDisRole(decodeTeam(roleChoice[1]))
                if(team==''):
                    team=roleChoice[1]
                if(team not in invalidRoles):
                    roleFound=False
                    for i in message.guild.roles:
                        if(team == i.name):   
                            user=message.author
                            await user.add_roles(i)
                            await message.channel.send("{} added to {}".format(team, message.author.mention))
                            roleFound=True
                            break
                    if(not roleFound):
                        await message.channel.send("Invalid Role")
                else:
                    await message.channel.send("Invalid Role")
        except discord.errors.Forbidden:
            await message.channel.send("Invalid Role")         
    if(message.content.startswith('?rroles')):
        roleChoice = message.content.split('?rroles ')
        try:
            if(len(roleChoice)==1):
                await message.channel.send("Enter a Role to Remove")
            else:
                team=convertTeamtoDisRole(decodeTeam(roleChoice[1]))
                if(team==''):
                    team=roleChoice[1]
                if(team not in invalidRoles):
                    roleFound=False
                    for i in message.guild.roles:
                        if(team == i.name):   
                            user=message.author
                            await user.remove_roles(i)
                            await message.channel.send("{} removed from {}".format(team, message.author.mention))
                            roleFound=True
                            break
                    if(not roleFound):
                        await message.channel.send("Invalid Role")
                else:
                    await message.channel.send("Invalid Role")
        except discord.errors.Forbidden:
            await message.channel.send("Invalid Role")
            
    # gifs and stuff
    if(message.content.startswith('?bu')):
            await message.channel.send("https://media.giphy.com/media/348tsqqVM1dCvT4zoY/source.mp4")
            
    if(message.content.startswith('?goodgoal')):
            await message.channel.send("https://gfycat.com/lastingcomplexblackbuck")
            
    if(message.content.startswith('?nogoal')):
            await message.channel.send("https://media.giphy.com/media/MTuCbbIEKUOxMiCp2z/source.gif")  

    if(message.content.startswith('?uml')):
            await message.channel.send("https://media.giphy.com/media/LqhaCKCh7E4WJrHZEE/source.mp4")
    
    if(message.content.startswith('?lowellbu')):
            await message.channel.send("https://media.giphy.com/media/Ss6tcZjgYgIpGMWKtS/giphy.gif")
            
    if(message.content.startswith('?harvard')):
            await message.channel.send("FUCK HARVARD")
        
    if(message.content.startswith('?boston')):
            gif="https://m.imgur.com/ZPZUGW0"
            random.seed(datetime.datetime.now())
            if(random.randint(0,100)<=10):
                gif="https://media.giphy.com/media/W2zqB99rxiTxDNT1Ci/giphy.gif"
            
            await message.channel.send(gif)
            
    if(message.content.startswith('?lowell') and not message.content.startswith('?lowellbu')):
            await message.channel.send("https://imgur.com/a/C9aSorC")
            
    if(message.content.startswith('?northdakota')):
            await message.channel.send("F'IN HAWKS")
            
    if(message.content.startswith('?bc')):
            await message.channel.send("https://imgur.com/a/mejC6E2")
            
    if(message.content.startswith('?uconn')):
            await message.channel.send("https://imgur.com/a/gWy8Ifj")
            
    if(message.content.startswith('?unh')):
            await message.channel.send("https://imgur.com/a/mq8brow")
            
    if(message.content.startswith('?mankato')):
            await message.channel.send("https://i.imgur.com/2B2iSkt.jpg")
            
    if(message.content.startswith('?ivyleague')):
            await message.channel.send("This command has to wait another couple weeks to start playing")
            
    if(message.content.startswith('?union')):
            await message.channel.send("https://imgur.com/a/ez3Pi5Q")
            
    if(message.content.startswith('?northeasternwins')):
            await message.channel.send("https://www.youtube.com/watch?v=RRVPTeL5udc")
            
    if(message.content.startswith('?michigantech')):
            await message.channel.send("http://www.johnsonsjerseys.net/temp/ncaa-2018.jpg")
            
    if(message.content.startswith('?nanooks')):
            await message.channel.send("https://www.youtube.com/watch?v=K9cYcRotufU")
            
    if(message.content.startswith('?lssu')):
            await message.channel.send("https://www.youtube.com/watch?v=HowMoUOhQSs")
            
    if(message.content.startswith('?gophers')):
            await message.channel.send("https://www.youtube.com/watch?v=X1_x1oo35L0")
            
    if(message.content.startswith('?miami')):
            await message.channel.send("https://youtu.be/_-mBI7jEfVU?t=81")
            
    if(message.content.startswith('?dartmouth')):
            await message.channel.send("https://www.youtube.com/watch?v=Qe3iNZjenvI")
            
    if(message.content.startswith('?pennstate')):
            await message.channel.send("https://imgur.com/a/uhqlM9S")
            
    if(message.content.startswith('?rpi')):
            await message.channel.send("https://imgur.com/uAndWDQ")
            
    if(message.content.startswith('?umass')):
            await message.channel.send("When they beat Providence tonight it will be legitimate proof that UMass deserves all of the recognition that it has received. They are 6-1 on the season and 3-0 in the conference which is an extremely impressive feat considering 2 years ago the team was not even ranked nationally.")
            
    if(message.content.startswith('?maine')):
            await message.channel.send("https://streamable.com/o1xmn")
            
    if(message.content.startswith('?bemidji')):
            await message.channel.send("https://www.youtube.com/watch?v=CW_B4KB0wYs")
            
    if(message.content.startswith('?nodak')):
            await message.channel.send("https://www.youtube.com/watch?v=-B2vE1Yl2_c")
            
    if(message.content.startswith('?mtu')):
            await message.channel.send("https://www.youtube.com/watch?v=FZQ6VNWvmOc")
    
    if(message.content.startswith('?denver')):
            await message.channel.send("https://media.giphy.com/media/XG7glHKnoBnTg57Sml/giphy.gif")
            
    if(message.content.startswith('?dog') or message.content.startswith('?doggo') or message.content.startswith('?doggy')):
            opt = message.content.split(' ')
            if(len(opt)>1):
                await message.channel.send(getDog(opt[1]))
            else:
                await message.channel.send(getDog(opt[0]))
    if(message.content.startswith('?cat') or message.content.startswith('?kitty')):         
        await message.channel.send(getCat())
        
    if(message.content.startswith('?hearef') or message.content.startswith('?heref')): 
        await message.channel.send('EXPERIENCE HOCKEY EAST OFFICIATING')
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    

def decodeTeam(team):
    origTeam = team
    team=team.lower()
    team=team.replace(" ","")
    team=team.replace("-","")
    team=team.replace("'","")
    team=team.replace(".","")
    if(team=='beanpot'):
        team = random.choice(['bu','bc','nu','hu'])
    dict={"afa" : "Air Force",
        "aic" : "American International",
        "alabamahuntsville" : "Alabama Huntsville",
        "americanintl" : "American International",
        "amworst" : "Massachusetts",
        "amwurst" : "Massachusetts",
        "anosu" : "Ohio State",
        "army" : "Army West Point",
        "asu" : "Arizona State",
        "bama" : "Alabama Huntsville",
        "bc" : "Boston College",
        "bemidji" : "Bemidji State",
        "bgsu" : "Bowling Green",
        "bigred" : "Cornell",
        "bobbymo" : "Robert Morris",
        "boston" : "Boston University",
        "bostonu" : "Boston University",
        "bowlinggreenstate" : "Bowling Green",
        "bruno" : "Brown",
        "bu" : "Boston University",
        "cambridgewarcriminalfactory" : "Harvard",
        "cc" : "Colorado College",
        "cgate" : "Colgate",
        "chestnuthillcommunitycollege" : "Boston College",
        "chestnuthilluniversity" : "Boston College",
        "clarky" : "Clarkson",
        "connecticut" : "UConn",
        "cor" : "Cornell",
        "cuse" : "Syracuse",
        "darty" : "Dartmouth",
        "du" : "Denver",
        "duluth" : "Minnesota Duluth",
        "dutchpeople" : "Union",
        "ferris" : "Ferris State",
        "ferriswheel" : "Ferris State",
        "finghawks" : "North Dakota",
        "goofers" : "Minnesota",
        "hc" : "Holy Cross",
        "hu" : "Harvard",
        "howlinhuskies" : "Northeastern",
        "huntsville" : "Alabama Huntsville",
        "icebus" : "UConn",
        "keggy" : "Dartmouth",
        "lakestate" : "Lake Superior State",
        "lakesuperior" : "Lake Superior State",
        "lowell" : "UMass Lowell",
        "lowelltech" : "UMass Lowell",
        "ulowell" : "Umass Lowell",
        "lssu" : "Lake Superior State",
        "lu" : "Lindenwood",
        "liu" : "Long Island University",
        "mack" : "Merrimack",
        "mankato" : "Minnesota State",
        "mc" : "Merrimack",
        "mich" : "Michigan",
        "meatchicken" : "Michigan",
        "mnsu" : "Minnesota State",
        "mrbee" : "American International",
        "msu" : "Michigan State",
        "mtu" : "Michigan Tech",
        "nd" : "Notre Dame",
        "nebraskaomaha" : "Omaha",
        "neu" : "Northeastern",
        "newtonsundayschool" : "Boston College",
        "newhavenwarcriminalfactory" : "Yale",
        "nmu" : "Northern Michigan",
        "northern" : "Northern Michigan",
        "nu" : "Northeastern",
        "osu" : "Ohio State",
        "pc" : "Providence",
        "pianohuskies" : "Michigan Tech",
        "prinny" : "Princeton",
        "psu" : "Penn State",
        "purplecows" : "Minnesota State",
        "qu" : "Quinnipiac",
        "quinny" : "Quinnipiac",
        "rmu" : "Robert Morris",
        "rpi" : "Rensselaer",
        "rit" : "RIT",
        "saintas" : "Saint Anselm",
        "scsu" : "St. Cloud State",
        "shu" : "Sacred Heart",
        "slu" : "St. Lawrence",
        "slushbus" : "UConn",
        "smc" : "Saint Michael's",
        "sparky" : "Arizona State",
        "sparty" : "Michigan State",
        "stanselm" : "Saint Anselm",
        "stcloud" : "St. Cloud State",
        "stmichaels" : "Saint Michael's",
        "stmikes" : "Saint Michael's",
        "sootech" : "Lake Superior State",
        "su" : "Syracuse",
        "syracuse" : "Syracuse",
        "toothpaste" : "Colgate",
        "uaa" : "Alaska Anchorage",
        "uaf" : "Air Force",
        "uaf" : "Alaska",
        "uah" : "Alabama Huntsville",
        "uconn" : "UConn",
        "umass" : "Massachusetts",
        "umassamherst" : "Massachusetts",
        "umasslowell" : "UMass Lowell",
        "umd" : "Minnesota Duluth",
        "uml" : "UMass Lowell",
        "umo" : "Maine",
        "umtc" : "Minnesota",
        "und" : "North Dakota",
        "unh" : "New Hampshire",
        "uno" : "Omaha",
        "usma" : "Army West Point",
        "uvm" : "Vermont",
        "uw" : "Wisconsin",
        "wisco" : "Wisconsin",
        "wmu" : "Western Michigan",
        "ziggy" : "Bowling Green",
        "zoomass" : "Massachusetts",
        "good": "Boston University",
        "bad" : "Boston College",
        "ugly" : "Harvard",
        "evil" : "Harvard",
        "ull" : "UL Lafayette",
        "ul" : "UL Lafayette",
        "louisiana" : "UL Lafayette",
        "georgiatech" : "Georgia Tech",
        "gt" : "Georgia Tech",
        "lsu" : "LSU",
        "ref" : "Ref",
        "refs" : "Ref",
        "stripes" : "Ref",
        "portal" : "Portal",
        "redsox" : "Red Sox",
        "yankees" : "Yankees",
        "meteor" : "Meteor",
        "jackbox" : "Jackbox",
        "usa" : "USA",
        "chaos" : "Chaos"}

    if team in dict:
        return dict[team]
    else:
        teamName=''
        teamSplit = origTeam.split(' ')
        for i in range(len(teamSplit)):
            teamName+=teamSplit[i].capitalize()
            if(i<len(teamSplit)-1):
                teamName+=' '
        return teamName
def generateScoreline(team, gender):
    global flairlist
    parser = MyHTMLParser()
    url = "http://collegehockeystats.net/"
    f=urllib.request.urlopen(url,timeout=10)
    html = f.read()
    f.close()
    parser.feed(html.decode("ISO-8859-1"))
    
    if("<meta HTTP-EQUIV=\"REFRESH\"" in html.decode("ISO-8859-1")):
        html = html.decode("ISO-8859-1")
        url=html.split("url=")
        url=url[1].split("\"")[0]
        f=urllib.request.urlopen(url,timeout = 10)
        html = f.read()
        f.close()
        parser.feed(html.decode("ISO-8859-1"))
    gameData=parser.return_data()

    days = gameData.split('\n\n')
    games = days[0].split('\n')
    #print(games)    
    mtagLookup = {}
    wtagLookup = {}
    leagues=set()
    gameList = []
    tag = ''
    for game in games:
        #print(game)
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
            if(game[0]==''):
                continue            
            if(game[0][0]=='('):
                tag=game[0]
                game.pop(0)                
        if(game.count('OT')>0):
            numOT = 'OT'
            if(game.count('2OT')>0):
                numOT = '2OT'
            elif(game.count('3OT')>0):
                numOT = '3OT'
            elif(game.count('4OT')>0):
                numOT = '4OT'
            game.pop(5)
            if(game.count('Final')>0):
                game[7]='Final ({})'.format(numOT)
        if(len(game)==8):
            game[5]=game[5].replace(' ',"")
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
          game[5]=game[5].replace(' ',"")
          if(game[5]=='EC,IV'):
            game[5] = 'EC'
          if(m_w == 'Women' and game[5]=='NH'):
              game[5] = 'NW'
          if(tag):
            if(m_w=='Men' and tag in list(mtagLookup.keys())):
              game[5]=mtagLookup[tag]
            if(m_w=='Women' and tag in list(wtagLookup.keys())):
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
            game[3]=game[3].replace(' ',"")
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
    games=gameList
    if scorebot.isD1(team,team,gender):
        for game in games:
            if((game['homeTeam'] == team or game['awayTeam'] == team) and game['m_w']==gender):            
                if("OT" in game['homeScore']):
                    if(game['homeScore'].count('OT')>0):
                        numOT = 'OT'
                        if(game['homeScore'].count('2OT')>0):
                            numOT = '2OT'
                        elif(game['homeScore'].count('3OT')>0):
                            numOT = '3OT'
                        elif(game['homeScore'].count('4OT')>0):
                            numOT = '4OT'
                    game['status']="Final ({})".format(numOT)
                    game['homeScore']=game['homeScore'].replace(numOT,"")
                if("TV-" in game['status']):
                    game['status']=re.sub(" \(TV-.*\) ","", game['status'])
                if(gender=='Men'):
                    winProb=getWinProb(game['awayTeam'],game['awayScore'],game['homeTeam'],game['homeScore'],game['status'])
                else:
                    winProb = ''
                if(game['awayTeam'] in flairlist):
                    game['awayTeam'] = flairlist[game['awayTeam']] + " " + game['awayTeam']
                if(game['homeTeam'] in flairlist):
                    game['homeTeam'] = flairlist[game['homeTeam']] + " " + game['homeTeam']

                scoreline= "{} {}\n{} {}\n{}".format(game['awayTeam'],game['awayScore'],game['homeTeam'],game['homeScore'],game['status'])
                if(winProb != ''):
                    scoreline+="\n\n> " + winProb
                return scoreline
        return "No game scheduled for {} {}".format(team,gender)
    return ":regional_indicator_x: Team Not Found"

def getDog(opt):
    opt=opt.lower()
    opt=opt.replace(' ','')
    if(opt=='bu' or opt == 'terrier' or opt == 'boston' or opt == 'bostonuniversity' or opt == 'bostonterrier'):
        url = "https://dog.ceo/api/breed/bulldog/boston/images/random"
    elif(opt == 'husky' or opt == 'nu' or opt == 'scsu' or opt == 'uconn' or opt == 'mtu'):
        url = "https://dog.ceo/api/breed/husky/images/random"
    elif(opt == 'ferris' or opt == 'bulldog' or opt == 'umd' or opt == 'yale'):
        url = "https://dog.ceo/api/breed/bulldog/english/images/random"
    else:
        url = "https://dog.ceo/api/breeds/image/random"
    j = json.load(urllib.request.urlopen(url))
    return j['message']
    
def getCat():
    url = "https://api.thecatapi.com/v1/images/search"
    j = json.load(urllib.request.urlopen(url))
    return j[0]['url']

def getSchedule(team,opt,gender):
    global season
    teamDict = {"Air Force" : "schedules/afa",
        "Alabama Huntsville" : "schedules/alh",
        "Alaska Anchorage" : "schedules/aka",
        "Alaska" : "schedules/akf",
        "American International" : "schedules/aic",
        "Arizona State" : "schedules/asu",
        "Army West Point" : "schedules/arm",
        "Bemidji State" : "schedules/bmj",
        "Bentley" : "schedules/ben",
        "Boston College" : "schedules/bc_",
        "Boston University" : "schedules/bu_",
        "Bowling Green" : "schedules/bgs",
        "Brown" : "schedules/brn",
        "Canisius" : "schedules/cns",
        "Clarkson" : "schedules/clk",
        "Colgate" : "schedules/clg",
        "Colorado College" : "schedules/cc_",
        "Cornell" : "schedules/cor",
        "Dartmouth" : "schedules/dar",
        "Denver" : "schedules/den",
        "Ferris State" : "schedules/fsu",
        "Franklin Pierce" : "schedules/fpu",
        "Harvard" : "schedules/har",
        "Holy Cross" : "schedules/hcr",
        "Lake Superior State" : "schedules/lss",
        "Lindenwood" : "schedules/lin",
        "Long Island University" : "schedules/liu",
        "Maine" : "schedules/mne",
        "Massachusetts" : "schedules/uma",
        "Mercyhurst" : "schedules/mrc",
        "Merrimack" : "schedules/mer",
        "Miami" : "schedules/mia",
        "Michigan State" : "schedules/msu",
        "Michigan Tech" : "schedules/mtu",
        "Michigan" : "schedules/mic",
        "Minnesota Duluth" : "schedules/mnd",
        "Minnesota State" : "schedules/mns",
        "Minnesota" : "schedules/min",
        "New Hampshire" : "schedules/unh",
        "Niagara" : "schedules/nia",
        "North Dakota" : "schedules/ndk",
        "Northeastern" : "schedules/noe",
        "Northern Michigan" : "schedules/nmu",
        "Notre Dame" : "schedules/ndm",
        "Ohio State" : "schedules/osu",
        "Omaha" : "schedules/uno",
        "Penn State" : "schedules/psu",
        "Post" : "schedules/pst",
        "Princeton" : "schedules/prn",
        "Providence" : "schedules/prv",
        "Quinnipiac" : "schedules/qui",
        "RIT" : "schedules/rit",
        "Rensselaer" : "schedules/ren",
        "Robert Morris" : "schedules/rmu",
        "Sacred Heart" : "schedules/sac",
        "Saint Anselm" : "schedules/sta",
        "Saint Michael's" : "schedules/stm",
        "St. Cloud State" : "schedules/stc",
        "St. Lawrence" : "schedules/stl",
        "Syracuse" : "schedules/syr",
        "UConn" : "schedules/con",
        "UMass Lowell" : "schedules/uml",
        "Union" : "schedules/uni",
        "Vermont" : "schedules/ver",
        "Western Michigan" : "schedules/wmu",
        "Wisconsin" : "schedules/wis",
        "Yale" : "schedules/yal"}
              
    decTeam = decodeTeam(team)
    if(scorebot.isD1(decTeam,decTeam,gender)):
        url = "http://www.collegehockeystats.net/{}/{}{}".format(season,teamDict[decTeam],gender[0].lower())
    else:
        return ":regional_indicator_x: Team Not Found"
    if(opt.isnumeric()):
        numGames = int(opt)
    else:
        numGames = 5
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]
    gameLine = '```'
    counter=0
    for i in table.find_all('tr'):
        game=i.find_all('td')
        if(len(game)>=7 and "Overall" not in game[-1].get_text() and "Sheet" not in game[-1].get_text()):
            counter+=1
            date=game[1].get_text()  
            opp=game[3].get_text()
            time=game[6].get_text()
            gameLine+="{} {} {}\n".format(date,opp,time)
        if(numGames<=counter):
            break
            
    gameLine +='```'
    if(gameLine=='``````'):
        return 'No Schedule Found'
    return gameLine
    
def getResults(team,opt,gender):
    teamDict = {"Air Force" : "schedules/afa",
        "Alabama Huntsville" : "schedules/alh",
        "Alaska Anchorage" : "schedules/aka",
        "Alaska" : "schedules/akf",
        "American International" : "schedules/aic",
        "Arizona State" : "schedules/asu",
        "Army West Point" : "schedules/arm",
        "Bemidji State" : "schedules/bmj",
        "Bentley" : "schedules/ben",
        "Boston College" : "schedules/bc_",
        "Boston University" : "schedules/bu_",
        "Bowling Green" : "schedules/bgs",
        "Brown" : "schedules/brn",
        "Canisius" : "schedules/cns",
        "Clarkson" : "schedules/clk",
        "Colgate" : "schedules/clg",
        "Colorado College" : "schedules/cc_",
        "Cornell" : "schedules/cor",
        "Dartmouth" : "schedules/dar",
        "Denver" : "schedules/den",
        "Ferris State" : "schedules/fsu",
        "Franklin Pierce" : "schedules/fpu",
        "Harvard" : "schedules/har",
        "Holy Cross" : "schedules/hcr",
        "Lake Superior State" : "schedules/lss",
        "Lindenwood" : "schedules/lin",
        "Long Island University" : "schedules/liu",
        "Maine" : "schedules/mne",
        "Massachusetts" : "schedules/uma",
        "Mercyhurst" : "schedules/mrc",
        "Merrimack" : "schedules/mer",
        "Miami" : "schedules/mia",
        "Michigan State" : "schedules/msu",
        "Michigan Tech" : "schedules/mtu",
        "Michigan" : "schedules/mic",
        "Minnesota Duluth" : "schedules/mnd",
        "Minnesota State" : "schedules/mns",
        "Minnesota" : "schedules/min",
        "New Hampshire" : "schedules/unh",
        "Niagara" : "schedules/nia",
        "North Dakota" : "schedules/ndk",
        "Northeastern" : "schedules/noe",
        "Northern Michigan" : "schedules/nmu",
        "Notre Dame" : "schedules/ndm",
        "Ohio State" : "schedules/osu",
        "Omaha" : "schedules/uno",
        "Penn State" : "schedules/psu",
        "Post" : "schedules/pst",
        "Princeton" : "schedules/prn",
        "Providence" : "schedules/prv",
        "Quinnipiac" : "schedules/qui",
        "RIT" : "schedules/rit",
        "Rensselaer" : "schedules/ren",
        "Robert Morris" : "schedules/rmu",
        "Sacred Heart" : "schedules/sac",
        "Saint Anselm" : "schedules/sta",
        "Saint Michael's" : "schedules/stm",
        "St. Cloud State" : "schedules/stc",
        "St. Lawrence" : "schedules/stl",
        "Syracuse" : "schedules/syr",
        "UConn" : "schedules/con",
        "UMass Lowell" : "schedules/uml",
        "Union" : "schedules/uni",
        "Vermont" : "schedules/ver",
        "Western Michigan" : "schedules/wmu",
        "Wisconsin" : "schedules/wis",
        "Yale" : "schedules/yal"}
              
    decTeam = decodeTeam(team)
    if(scorebot.isD1(decTeam,decTeam,gender)):
       url = "http://www.collegehockeystats.net/{}/{}{}".format(season,teamDict[decTeam],gender[0].lower())
    else:
        return ":regional_indicator_x: Team Not Found"
    if(opt.isnumeric()):
        numGames = int(opt)
    else:
        numGames = 5
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]
    gameLine = '```'
    counter=0
    games = []
    for i in table.find_all('tr'):
        game=i.find_all('td')
        if(len(game)>=7 and "Overall" in game[-1].get_text() or "Sheet" in game[-1].get_text()):
            counter+=1
            date=game[1].get_text()  
            opp=game[3].get_text()
            time=game[6].get_text()
            result=''
            for i in range(5,11):
                result+=game[i].get_text()
            gamesData = "{} {} {}\n".format(date,opp,result)
            games.append(gamesData)
            
    numGames *= -1
    gamesToReport = games[numGames:]
    for i in gamesToReport:
        gameLine+= i
            
    gameLine +='```'
    if(gameLine=='``````'):
        return 'No Results Found'
    return gameLine
client.run(TOKEN)
print("Ending... at",datetime.datetime.now())
