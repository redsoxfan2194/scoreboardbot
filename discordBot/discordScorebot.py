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
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
season = '1819'
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
#flairlist = {}
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
?[whatsontv] - displays list of Today's games broadcasted on TV
?[thanksbot] - Thanks Bot
?[roles] - display list of availible roles
?[roles] [role/team name] - adds role to user
?[rroles] [role/team name] - removes role from user

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
                "Long Island" : "LIU Sharks",
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
    "UConn Huskies" : ["Go Huskies!", "U-C-O-N-N UCONN UCONN UCONN"],
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
    "UMass Minutemen" : ["Please Don't Riot!", "We Last Longer!","Think of those couches...they have family", "Embarrassment of the Commonwealth"],
    "Boston University Terriers" : ["Sucks to BU!", "Screw BU!"],
    "Northeastern Huskies" : ["Northleastern", "North! Eastern! Sucks!"],
    "Colgate Raiders" : ["Crest is Best!"],
    "Cornell Big Red" : ["Harvard Rejects!", "```Up above Cayuga's waters, there's an awful smell;\nThirty thousand Harvard rejects call themselves Cornell.\nFlush the toilet, flush the toilet,\nFlush them all to hell!\nThirty thousand Harvard rejects call themselves Cornell!```"],
    "Maine Black Bears" : ["M-A-I-N-E ~~Go Blue~~ MAAAAAIIINNNE SUCKS"],
    "Louisiana State University Tigers" :["Louisiana State University and Agricultural and Mechanical College"],
    "Wisconsin Badgers" : ["Dirty Sconnies"],
    "Michigan State Spartans" : ["Poor Sparty"],
    "Notre Dame Fighting Irish" : ["Blinded by the Light", "Notre Lame!", "Rudy was offsides!"],
    "St. Cloud State Huskies" : ["Go back to Montreal!", "St. Cloud Sucks!"],
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
    
            
        
    winLookup={'0': ['0', '0', '0', '0', '0', '0', '0'], '5': ['0.895059121621622', '0', '0', '0', '0', '0', '0'], '10': ['0.895604395604396', '0.25', '0', '0', '0', '0', '0'], '15': ['0.895329087048832', '0.538461538461538', '0', '0', '0', '0', '0'], '20': ['0.895063047659756', '0.68421052631579', '0', '0', '0', '0', '0'], '25': ['0.895358831113021', '0.585365853658537', '0', '0', '0', '0', '0'], '30': ['0.895477169443843', '0.614035087719298', '1', '0', '0', '0', '0'], '35': ['0.895171813832101', '0.583941605839416', '1', '0', '0', '0', '0'], '40': ['0.89501312335958', '0.574074074074074', '1', '0', '0', '0', '0'], '45': ['0.894505494505495', '0.568306010928962', '1', '0', '0', '0', '0'], '50': ['0.894096838381605', '0.542857142857143', '1', '0', '0', '0', '0'], '55': ['0.893986636971047', '0.518518518518518', '1', '0', '0', '0', '0'], '60': ['0.894336243563913', '0.528301886792453', '1', '0', '0', '0', '0'], '65': ['0.894085900607151', '0.519434628975265', '1', '0', '0', '0', '0'], '70': ['0.89372309086789', '0.487341772151899', '1', '0', '0', '0', '0'], '75': ['0.893714285714286', '0.484419263456091', '1', '0', '0', '0', '0'], '80': ['0.893768682455737', '0.468253968253968', '1', '0', '0', '0', '0'], '85': ['0.893351800554017', '0.460759493670886', '1', '0', '0', '0', '0'], '90': ['0.893636785880167', '0.463007159904535', '1', '0', '0', '0', '0'], '95': ['0.893249240831581', '0.471655328798186', '0.928571428571429', '0', '0', '0', '0'], '100': ['0.893201599623618', '0.464968152866242', '0.928571428571429', '0', '0', '0', '0'], '105': ['0.892992424242424', '0.462626262626263', '0.9375', '1', '0', '0', '0'], '110': ['0.892465426800191', '0.464627151051625', '0.888888888888889', '1', '0', '0', '0'], '115': ['0.892754318618042', '0.471766848816029', '0.888888888888889', '1', '0', '0', '0'], '120': ['0.892055059164453', '0.465968586387435', '0.904761904761905', '1', '0', '0', '0'], '125': ['0.891806467298809', '0.45575959933222', '0.91304347826087', '1', '0', '0', '0'], '130': ['0.891984359726295', '0.461165048543689', '0.92', '1', '0', '0', '0'], '135': ['0.892051030421982', '0.466772151898734', '0.925925925925926', '1', '0', '0', '0'], '140': ['0.891851851851852', '0.458015267175573', '0.866666666666667', '1', '0', '0', '0'], '145': ['0.892066650087043', '0.449339207048458', '0.878787878787879', '1', '0', '0', '0'], '150': ['0.891858141858142', '0.440459110473458', '0.823529411764706', '1', '0', '0', '0'], '155': ['0.891675025075226', '0.451339915373766', '0.736842105263158', '1', '0', '0', '0'], '160': ['0.891435768261965', '0.448275862068966', '0.75', '1', '0', '0', '0'], '165': ['0.891304347826087', '0.436906377204885', '0.761904761904762', '1', '0', '0', '0'], '170': ['0.891260162601626', '0.423076923076923', '0.772727272727273', '1', '0', '0', '0'], '175': ['0.890676883780332', '0.428571428571429', '0.693877551020408', '1', '0', '0', '0'], '180': ['0.890200102616726', '0.432397959183674', '0.692307692307692', '1', '0', '0', '0'], '185': ['0.889576883384933', '0.433374844333748', '0.709090909090909', '1', '0', '0', '0'], '190': ['0.889033264033264', '0.43719806763285', '0.724137931034483', '1', '0', '0', '0'], '195': ['0.888975966562173', '0.427725118483412', '0.725806451612903', '1', '0', '0', '0'], '200': ['0.889472302441586', '0.419091967403958', '0.742424242424242', '1', '0', '0', '0'], '205': ['0.889152810768013', '0.409350057012543', '0.720588235294118', '1', '0', '0', '0'], '210': ['0.88936170212766', '0.409745293466224', '0.690140845070423', '1', '0', '0', '0'], '215': ['0.888471849865952', '0.393776824034335', '0.694444444444444', '1', '0', '0', '0'], '220': ['0.8887092427917', '0.39662447257384', '0.702702702702703', '1', '0', '0', '0'], '225': ['0.888648062855595', '0.403726708074534', '0.710526315789474', '1', '0', '0', '0'], '230': ['0.888193688792165', '0.403076923076923', '0.731707317073171', '1', '0', '0', '0'], '235': ['0.887975897014517', '0.398194583751254', '0.741176470588235', '1', '0', '0', '0'], '240': ['0.887110129726746', '0.403131115459883', '0.75', '1', '0', '0', '0'], '245': ['0.886792452830189', '0.403660886319846', '0.755555555555556', '1', '0', '0', '0'], '250': ['0.887367244270542', '0.408317580340265', '0.752577319587629', '1', '0', '0', '0'], '255': ['0.887608878898567', '0.410614525139665', '0.76', '1', '0', '0', '0'], '260': ['0.887729196050776', '0.412903225806452', '0.774509803921569', '0.75', '0', '0', '0'], '265': ['0.887279954571266', '0.413730803974706', '0.766990291262136', '0.75', '0', '0', '0'], '270': ['0.88685190489831', '0.417766051011434', '0.778846153846154', '0.75', '0', '0', '0'], '275': ['0.886901327178303', '0.413494809688581', '0.763636363636364', '0.75', '0', '0', '0'], '280': ['0.886211901306241', '0.413117546848382', '0.761061946902655', '0.75', '0', '0', '0'], '285': ['0.886231038506418', '0.418487394957983', '0.752212389380531', '0.8', '0', '0', '0'], '290': ['0.885630498533724', '0.415282392026578', '0.741379310344828', '0.833333333333333', '0', '0', '0'], '295': ['0.885149099498081', '0.41469387755102', '0.743589743589744', '0.857142857142857', '0', '0', '0'], '300': ['0.884958382877527', '0.416935483870968', '0.744', '0.857142857142857', '0', '0', '0'], '305': ['0.884235716422375', '0.423015873015873', '0.746031746031746', '0.857142857142857', '0', '0', '0'], '310': ['0.883966244725738', '0.41796875', '0.755725190839695', '0.857142857142857', '0', '0', '0'], '315': ['0.883742052679382', '0.408985282726569', '0.755555555555556', '0.857142857142857', '0', '0', '0'], '320': ['0.883912248628885', '0.413608562691131', '0.726618705035971', '0.857142857142857', '0', '0', '0'], '325': ['0.884155684952498', '0.40785498489426', '0.732394366197183', '0.857142857142857', '0', '0', '0'], '330': ['0.88434327899108', '0.410969196093163', '0.73972602739726', '0.875', '0', '0', '0'], '335': ['0.885103747290183', '0.409799554565702', '0.748344370860927', '0.888888888888889', '0', '0', '0'], '340': ['0.883945239576851', '0.417647058823529', '0.745098039215686', '0.888888888888889', '0', '0', '0'], '345': ['0.884039900249377', '0.420512820512821', '0.745098039215686', '0.9', '0', '0', '0'], '350': ['0.884880803011292', '0.420899854862119', '0.729559748427673', '0.909090909090909', '0', '0', '0'], '355': ['0.884748973792232', '0.421203438395416', '0.732919254658385', '0.916666666666667', '0', '0', '0'], '360': ['0.884126984126984', '0.419034090909091', '0.727272727272727', '0.923076923076923', '0', '0', '0'], '365': ['0.883312020460358', '0.416432584269663', '0.719298245614035', '0.923076923076923', '0', '0', '0'], '370': ['0.883541867179981', '0.416899441340782', '0.724137931034483', '0.923076923076923', '0', '0', '0'], '375': ['0.883720930232558', '0.423529411764706', '0.708791208791209', '0.923076923076923', '0', '0', '0'], '380': ['0.883517196625568', '0.421885753613214', '0.705882352941176', '0.928571428571429', '0', '0', '0'], '385': ['0.883849918433931', '0.417349726775956', '0.713541666666667', '0.933333333333333', '0', '0', '0'], '390': ['0.883300460223537', '0.418745785569791', '0.709183673469388', '0.933333333333333', '0', '0', '0'], '395': ['0.8833607907743', '0.414814814814815', '0.706467661691542', '0.933333333333333', '0', '0', '0'], '400': ['0.883172917358115', '0.410153640614562', '0.710900473933649', '0.933333333333333', '0', '0', '0'], '405': ['0.883798140770252', '0.412985274431058', '0.705607476635514', '0.9375', '0', '0', '0'], '410': ['0.88376753507014', '0.411803713527851', '0.708333333333333', '0.944444444444444', '0', '0', '0'], '415': ['0.883417085427136', '0.410714285714286', '0.711009174311927', '0.952380952380952', '0', '0', '0'], '420': ['0.883125631525766', '0.406824146981627', '0.714932126696833', '0.954545454545455', '0', '0', '0'], '425': ['0.882852292020374', '0.409974093264249', '0.716814159292035', '0.95', '1', '0', '0'], '430': ['0.882513661202186', '0.410404624277457', '0.710526315789474', '0.954545454545455', '1', '0', '0'], '435': ['0.882777586799588', '0.408253968253968', '0.716157205240175', '0.954545454545455', '1', '0', '0'], '440': ['0.882067291016302', '0.40613266583229', '0.718614718614719', '0.956521739130435', '1', '0', '0'], '445': ['0.882989870764932', '0.405321782178218', '0.71551724137931', '0.958333333333333', '1', '0', '0'], '450': ['0.882373595505618', '0.405521472392638', '0.716738197424893', '0.958333333333333', '1', '0', '0'], '455': ['0.883245149911816', '0.407294832826748', '0.714285714285714', '0.958333333333333', '1', '0', '0'], '460': ['0.882352941176471', '0.408679927667269', '0.717391304347826', '0.958333333333333', '1', '0', '0'], '465': ['0.881743479814219', '0.407142857142857', '0.719827586206897', '0.958333333333333', '1', '0', '0'], '470': ['0.881362007168459', '0.404394299287411', '0.721518987341772', '0.958333333333333', '1', '0', '0'], '475': ['0.880446525027008', '0.399527186761229', '0.726141078838174', '0.96', '1', '0', '0'], '480': ['0.880057803468208', '0.401769911504425', '0.731707317073171', '0.961538461538462', '1', '0', '0'], '485': ['0.879956347762823', '0.40058651026393', '0.723320158102767', '0.962962962962963', '1', '0', '0'], '490': ['0.879253567508233', '0.400583090379009', '0.712062256809339', '0.96551724137931', '1', '0', '0'], '495': ['0.879367414490621', '0.396292004634994', '0.715384615384615', '0.96551724137931', '1', '0', '0'], '500': ['0.877967359050445', '0.397824842587292', '0.718146718146718', '0.96875', '1', '0', '0'], '505': ['0.877140729709605', '0.392694063926941', '0.712121212121212', '0.96875', '1', '0', '0'], '510': ['0.8773373223635', '0.396022727272727', '0.709433962264151', '0.914285714285714', '1', '0', '0'], '515': ['0.877719429857464', '0.4', '0.697761194029851', '0.914285714285714', '1', '0', '0'], '520': ['0.877643504531722', '0.402021336327906', '0.692592592592593', '0.914285714285714', '1', '0', '0'], '525': ['0.877186311787072', '0.403118040089087', '0.695970695970696', '0.911764705882353', '1', '0', '0'], '530': ['0.877714285714286', '0.406023424428332', '0.691756272401434', '0.914285714285714', '1', '0', '0'], '535': ['0.877112135176651', '0.403314917127072', '0.685714285714286', '0.921052631578947', '1', '0', '0'], '540': ['0.877314814814815', '0.407284768211921', '0.681660899653979', '0.921052631578947', '1', '0', '0'], '545': ['0.876648564778898', '0.406798245614035', '0.682758620689655', '0.923076923076923', '1', '0', '0'], '550': ['0.876509544215037', '0.409934497816594', '0.685121107266436', '0.906976744186046', '1', '0', '0'], '555': ['0.876760563380282', '0.409140369967356', '0.68135593220339', '0.902439024390244', '1', '0', '0'], '560': ['0.87652379079827', '0.411382113821138', '0.677740863787375', '0.902439024390244', '1', '0', '0'], '565': ['0.87613771270281', '0.408108108108108', '0.669871794871795', '0.902439024390244', '1', '0', '0'], '570': ['0.876194267515923', '0.408064516129032', '0.675078864353312', '0.902439024390244', '1', '0', '0'], '575': ['0.876255524306951', '0.402127659574468', '0.678125', '0.902439024390244', '1', '0', '0'], '580': ['0.876263647391832', '0.400634249471459', '0.673913043478261', '0.906976744186046', '1', '0', '0'], '585': ['0.876623376623377', '0.399683210137276', '0.688073394495413', '0.869565217391304', '1', '0', '0'], '590': ['0.876885446392173', '0.393026941362916', '0.70414201183432', '0.872340425531915', '1', '0', '0'], '595': ['0.876897825194912', '0.392218717139853', '0.704678362573099', '0.875', '1', '0', '0'], '600': ['0.878800328677075', '0.395997893628225', '0.704022988505747', '0.875', '1', '0', '0'], '605': ['0.878586278586278', '0.393860561914672', '0.69971671388102', '0.877551020408163', '1', '0', '0'], '610': ['0.877967513536027', '0.390307451797811', '0.704735376044568', '0.88', '1', '0', '0'], '615': ['0.877661795407098', '0.3911227154047', '0.70189701897019', '0.88', '1', '0', '0'], '620': ['0.876677852348993', '0.389380530973451', '0.705882352941176', '0.88', '1', '0', '0'], '625': ['0.877104377104377', '0.388541666666667', '0.704960835509138', '0.88', '1', '0', '0'], '630': ['0.876903553299492', '0.384735202492212', '0.702842377260982', '0.884615384615385', '1', '0', '0'], '635': ['0.875691783737761', '0.384496124031008', '0.713554987212276', '0.851851851851852', '1', '0', '0'], '640': ['0.875053304904051', '0.38270326255826', '0.719298245614035', '0.849056603773585', '1', '0', '0'], '645': ['0.875', '0.384734399174832', '0.716748768472906', '0.818181818181818', '1', '0', '0'], '650': ['0.875160875160875', '0.392227979274611', '0.714634146341463', '0.821428571428571', '1', '0', '0'], '655': ['0.87526789541363', '0.393229166666667', '0.715311004784689', '0.818181818181818', '1', '0', '0'], '660': ['0.875484704868591', '0.395844155844156', '0.719339622641509', '0.785714285714286', '1', '0', '0'], '665': ['0.874891774891775', '0.398858921161826', '0.717289719626168', '0.8', '1', '0', '0'], '670': ['0.874022589052997', '0.397302904564315', '0.730414746543779', '0.774193548387097', '1', '0', '0'], '675': ['0.873092019188836', '0.396275219865494', '0.727064220183486', '0.78125', '1', '0', '0'], '680': ['0.872368421052632', '0.392672858617131', '0.722972972972973', '0.78125', '1', '0', '0'], '685': ['0.871308946672543', '0.392197125256673', '0.736363636363636', '0.738461538461539', '1', '0', '0'], '690': ['0.872283813747228', '0.395610005104645', '0.741496598639456', '0.716417910447761', '1', '0', '0'], '695': ['0.871875', '0.396542958820539', '0.732142857142857', '0.716417910447761', '1', '0', '0'], '700': ['0.872597228430934', '0.395727365208545', '0.732891832229581', '0.712121212121212', '1', '0', '0'], '705': ['0.87342908438061', '0.398171660741493', '0.730853391684901', '0.720588235294118', '1', '0', '0'], '710': ['0.872858431018936', '0.401515151515152', '0.736725663716814', '0.732394366197183', '1', '0', '0'], '715': ['0.873023045639403', '0.404244567963618', '0.733041575492341', '0.736111111111111', '1', '0', '0'], '720': ['0.872571170356981', '0.404568527918782', '0.731759656652361', '0.736111111111111', '1', '0', '0'], '725': ['0.872842870118074', '0.405775075987842', '0.726114649681529', '0.77027027027027', '1', '0', '0'], '730': ['0.873175182481752', '0.405255179383527', '0.727848101265823', '0.776315789473684', '1', '0', '0'], '735': ['0.87265231333028', '0.405555555555556', '0.735966735966736', '0.776315789473684', '1', '0', '0'], '740': ['0.872183908045977', '0.404846037354871', '0.738144329896907', '0.784810126582278', '1', '0', '0'], '745': ['0.871593533487298', '0.407164480322906', '0.734279918864097', '0.7875', '1', '0', '0'], '750': ['0.871296296296296', '0.409182643794147', '0.736418511066398', '0.7875', '1', '0', '0'], '755': ['0.870232558139535', '0.409456740442656', '0.742', '0.790123456790123', '1', '0', '0'], '760': ['0.870154133582438', '0.405826217980914', '0.747514910536779', '0.797619047619048', '1', '0', '0'], '765': ['0.870544090056285', '0.407425990968389', '0.749506903353057', '0.802325581395349', '1', '0', '0'], '770': ['0.86987270155587', '0.409204602301151', '0.75146771037182', '0.804597701149425', '1', '0', '0'], '775': ['0.869606448553817', '0.406593406593407', '0.759152215799615', '0.806818181818182', '1', '0', '0'], '780': ['0.869544592030361', '0.407407407407407', '0.759615384615385', '0.813186813186813', '1', '0', '0'], '785': ['0.87', '0.404595404595405', '0.764367816091954', '0.817204301075269', '1', '0', '0'], '790': ['0.872309899569584', '0.402390438247012', '0.768642447418738', '0.821052631578947', '1', '0', '0'], '795': ['0.87236084452975', '0.404075546719682', '0.766159695817491', '0.842105263157895', '1', '1', '0'], '800': ['0.873435996150144', '0.400298359025361', '0.769811320754717', '0.816326530612245', '1', '1', '0'], '805': ['0.873852102464959', '0.399801587301587', '0.770676691729323', '0.82', '1', '1', '0'], '810': ['0.873607748184019', '0.399205561072493', '0.77196261682243', '0.82', '1', '1', '0'], '815': ['0.87311618862421', '0.400693412580485', '0.776119402985075', '0.821782178217822', '1', '1', '0'], '820': ['0.87311618862421', '0.403073872087258', '0.773831775700935', '0.817307692307692', '1', '1', '0'], '825': ['0.874088478366553', '0.406156901688183', '0.775092936802974', '0.825242718446602', '1', '1', '0'], '830': ['0.874146341463415', '0.40505701536936', '0.77037037037037', '0.828571428571429', '1', '1', '0'], '835': ['0.8737721021611', '0.403950617283951', '0.772477064220183', '0.830188679245283', '1', '1', '0'], '840': ['0.873891625615764', '0.404549950544016', '0.770909090909091', '0.834862385321101', '1', '1', '0'], '845': ['0.87382483918852', '0.405925925925926', '0.771739130434783', '0.839285714285714', '1', '1', '0'], '850': ['0.87394540942928', '0.401975308641975', '0.779174147217235', '0.831858407079646', '1', '1', '0'], '855': ['0.873941205779771', '0.401679841897233', '0.780141843971631', '0.834782608695652', '1', '1', '0'], '860': ['0.873373373373373', '0.399802078179119', '0.773519163763066', '0.854700854700855', '1', '1', '0'], '865': ['0.874622356495468', '0.403154263183834', '0.760416666666667', '0.873949579831933', '1', '1', '0'], '870': ['0.875694795351187', '0.41025641025641', '0.755593803786575', '0.883333333333333', '0.961538461538462', '1', '0'], '875': ['0.875126903553299', '0.40994094488189', '0.758561643835616', '0.867768595041322', '0.962962962962963', '1', '0'], '880': ['0.873604060913705', '0.411330049261084', '0.757264957264957', '0.867768595041322', '0.964285714285714', '1', '0'], '885': ['0.874680306905371', '0.413470993117011', '0.757983193277311', '0.867768595041322', '0.96551724137931', '1', '0'], '890': ['0.874297393970363', '0.415475603745688', '0.758793969849246', '0.868852459016393', '0.96551724137931', '1', '0'], '895': ['0.874358974358974', '0.418387413962635', '0.758793969849246', '0.869918699186992', '0.966666666666667', '1', '0'], '900': ['0.873203285420945', '0.420510304219823', '0.763912310286678', '0.872', '0.966666666666667', '1', '0'], '905': ['0.873515745998967', '0.420048899755501', '0.763422818791946', '0.873015873015873', '0.966666666666667', '1', '0'], '910': ['0.872868217054264', '0.42360430950049', '0.76126878130217', '0.875968992248062', '0.964285714285714', '1', '0'], '915': ['0.8717683557394', '0.424926398429833', '0.754966887417219', '0.874015748031496', '0.966666666666667', '1', '0'], '920': ['0.87111801242236', '0.425406203840473', '0.751633986928105', '0.890625', '0.966666666666667', '1', '0'], '925': ['0.870109546165884', '0.424301812836845', '0.753246753246753', '0.891472868217054', '0.966666666666667', '1', '0'], '930': ['0.870748299319728', '0.423246689553703', '0.754807692307692', '0.891472868217054', '0.96551724137931', '1', '0'], '935': ['0.869701726844584', '0.427236971484759', '0.754777070063694', '0.892307692307692', '0.96551724137931', '1', '0'], '940': ['0.868628481345244', '0.424987702902115', '0.759433962264151', '0.892307692307692', '0.966666666666667', '1', '0'], '945': ['0.869267264101212', '0.425971470732907', '0.755451713395639', '0.892307692307692', '0.966666666666667', '1', '0'], '950': ['0.868740115972588', '0.427375677006401', '0.752738654147105', '0.896296296296296', '0.966666666666667', '1', '0'], '955': ['0.868393234672304', '0.427939006394491', '0.752738654147105', '0.897810218978102', '0.967741935483871', '1', '0'], '960': ['0.867764206054169', '0.427027027027027', '0.751159196290572', '0.911764705882353', '0.967741935483871', '1', '0'], '965': ['0.868155236576289', '0.427728613569322', '0.752321981424149', '0.907142857142857', '1', '1', '0'], '970': ['0.868336886993603', '0.424704724409449', '0.759630200308166', '0.909722222222222', '1', '1', '0'], '975': ['0.868869936034115', '0.427165354330709', '0.758887171561051', '0.910344827586207', '1', '1', '0'], '980': ['0.868237814675951', '0.429833169774289', '0.758887171561051', '0.912162162162162', '1', '1', '0'], '985': ['0.868958109559613', '0.430958230958231', '0.755725190839695', '0.912162162162162', '1', '1', '0'], '990': ['0.867995689655172', '0.433628318584071', '0.75531914893617', '0.912751677852349', '1', '1', '0'], '995': ['0.867567567567568', '0.436086529006883', '0.748484848484849', '0.913333333333333', '1', '1', '0'], '1000': ['0.867136659436009', '0.4375', '0.745508982035928', '0.912751677852349', '1', '1', '0'], '1005': ['0.866666666666667', '0.436978911230996', '0.743703703703704', '0.919463087248322', '1', '1', '0'], '1010': ['0.866447728516694', '0.433415233415233', '0.744493392070485', '0.92', '1', '1', '0'], '1015': ['0.866081229418222', '0.432299359921221', '0.743813682678312', '0.92156862745098', '1', '1', '0'], '1020': ['0.865934065934066', '0.432165762210163', '0.742028985507246', '0.923076923076923', '1', '1', '0'], '1025': ['0.865088105726872', '0.432178217821782', '0.744285714285714', '0.923566878980892', '1', '1', '0'], '1030': ['0.866115702479339', '0.428997020854022', '0.748221906116643', '0.91875', '1', '1', '0'], '1035': ['0.867217630853994', '0.429706905116741', '0.752503576537911', '0.908536585365854', '1', '1', '0'], '1040': ['0.866407982261641', '0.427722772277228', '0.746418338108883', '0.910714285714286', '1', '1', '0'], '1045': ['0.86729594669628', '0.425037110341415', '0.743919885550787', '0.910714285714286', '1', '1', '0'], '1050': ['0.867671691792295', '0.424197530864198', '0.742165242165242', '0.912280701754386', '1', '1', '0'], '1055': ['0.867523756288429', '0.421936758893281', '0.748221906116643', '0.912790697674419', '1', '1', '0'], '1060': ['0.866292134831461', '0.421156697973307', '0.747887323943662', '0.913793103448276', '1', '1', '0'], '1065': ['0.866066404051773', '0.419594260267195', '0.748948106591865', '0.914772727272727', '1', '1', '0'], '1070': ['0.865874363327674', '0.425542406311637', '0.744022503516174', '0.917127071823204', '1', '1', '0'], '1075': ['0.86503416856492', '0.423778983719783', '0.741258741258741', '0.920634920634921', '1', '1', '0'], '1080': ['0.864387464387464', '0.425962487660415', '0.741620111731844', '0.921052631578947', '1', '1', '0'], '1085': ['0.864338866628506', '0.423929098966027', '0.746143057503506', '0.913265306122449', '1', '1', '0'], '1090': ['0.865051903114187', '0.426052889324192', '0.744022503516174', '0.914572864321608', '1', '1', '0'], '1095': ['0.865162037037037', '0.426966292134831', '0.743300423131171', '0.914572864321608', '1', '1', '0'], '1100': ['0.864219114219114', '0.428223844282238', '0.740479548660085', '0.916256157635468', '1', '1', '0'], '1105': ['0.86400937866354', '0.429334628460418', '0.734550561797753', '0.927184466019417', '1', '1', '0'], '1110': ['0.863529411764706', '0.429679922405432', '0.73314606741573', '0.92822966507177', '1', '1', '0'], '1115': ['0.863046044864227', '0.428918000970403', '0.732492997198879', '0.929577464788732', '1', '1', '0'], '1120': ['0.863582443653618', '0.430858806404658', '0.729166666666667', '0.930232558139535', '1', '1', '0'], '1125': ['0.863771564544914', '0.431619786614937', '0.727524204702628', '0.930232558139535', '1', '1', '0'], '1130': ['0.862768496420048', '0.432380029083858', '0.734159779614325', '0.930232558139535', '1', '1', '0'], '1135': ['0.862418106015485', '0.4356483729966', '0.733425414364641', '0.930875576036866', '1', '1', '0'], '1140': ['0.863283582089552', '0.434677027683341', '0.733793103448276', '0.931506849315068', '1', '1', '0'], '1145': ['0.862089552238806', '0.4356483729966', '0.738589211618257', '0.931506849315068', '1', '1', '0'], '1150': ['0.862545018007203', '0.429679922405432', '0.736551724137931', '0.932735426008969', '1', '1', '0'], '1155': ['0.861612515042118', '0.4273919378339', '0.739368998628258', '0.928888888888889', '1', '1', '0'], '1160': ['0.859891761876127', '0.428292682926829', '0.740791268758527', '0.929824561403509', '1', '1', '0'], '1165': ['0.860507246376812', '0.430238210986874', '0.73734610123119', '0.930131004366812', '1', '1', '0'], '1170': ['0.862756952841596', '0.428362573099415', '0.736698499317872', '0.931623931623932', '1', '1', '0'], '1175': ['0.862089914945322', '0.424257184607891', '0.73806275579809', '0.925311203319502', '1', '1', '0'], '1180': ['0.86019536019536', '0.423563777994158', '0.737127371273713', '0.925925925925926', '1', '1', '0'], '1185': ['0.859076923076923', '0.423392943450943', '0.737997256515775', '0.928571428571429', '1', '1', '0'], '1190': ['0.859259259259259', '0.419932268988873', '0.738775510204082', '0.928571428571429', '1', '1', '0'], '1195': ['0.861128332300062', '0.420696324951644', '0.731443994601889', '0.936254980079681', '1', '1', '0'], '1200': ['0.861509669369931', '0.424154589371981', '0.733957219251337', '0.940239043824701', '1', '1', '0'], '1205': ['0.861509669369931', '0.424154589371981', '0.733957219251337', '0.940239043824701', '1', '1', '0'], '1210': ['0.861423220973783', '0.423597678916828', '0.735019973368842', '0.940239043824701', '1', '1', '0'], '1215': ['0.862327909887359', '0.421663442940039', '0.735019973368842', '0.940944881889764', '1', '1', '0'], '1220': ['0.862437185929648', '0.421459642339294', '0.732804232804233', '0.937007874015748', '1', '1', '0'], '1225': ['0.862025316455696', '0.418470418470418', '0.736702127659574', '0.934362934362934', '1', '1', '0'], '1230': ['0.862857142857143', '0.417630057803468', '0.73474801061008', '0.943181818181818', '1', '1', '0'], '1235': ['0.863318499682136', '0.421611191509889', '0.731836195508586', '0.943181818181818', '1', '1', '0'], '1240': ['0.863346104725415', '0.420596727622714', '0.732542819499341', '0.942965779467681', '1', '1', '0'], '1245': ['0.863636363636364', '0.424783027965284', '0.72870249017038', '0.935606060606061', '1', '1', '0'], '1250': ['0.86529826812059', '0.425675675675676', '0.727509778357236', '0.935361216730038', '1', '1', '0'], '1255': ['0.861757105943152', '0.423745173745174', '0.730322580645161', '0.928030303030303', '1', '1', '1'], '1260': ['0.862024500322373', '0.428986912263694', '0.722151088348271', '0.927480916030534', '1', '1', '1'], '1265': ['0.860480207657365', '0.428019323671498', '0.720870678617157', '0.928301886792453', '1', '1', '1'], '1270': ['0.860602094240838', '0.428502648050072', '0.717752234993614', '0.929368029739777', '1', '1', '1'], '1275': ['0.860158311345646', '0.427884615384615', '0.720253164556962', '0.929368029739777', '1', '1', '1'], '1280': ['0.861037234042553', '0.42678828612578', '0.716436637390213', '0.92910447761194', '1', '1', '1'], '1285': ['0.861702127659574', '0.427338129496403', '0.720959595959596', '0.929889298892989', '1', '1', '1'], '1290': ['0.860279441117764', '0.430894308943089', '0.723566878980892', '0.93040293040293', '1', '1', '1'], '1295': ['0.861073825503356', '0.435299714557564', '0.717029449423816', '0.931159420289855', '1', '1', '1'], '1300': ['0.861185983827493', '0.43699476937708', '0.717752234993614', '0.931654676258993', '1', '1', '1'], '1305': ['0.861601085481682', '0.437855787476281', '0.71501272264631', '0.935018050541516', '1', '1', '1'], '1310': ['0.859565807327001', '0.441539923954373', '0.714467005076142', '0.935483870967742', '1', '1', '1'], '1315': ['0.859279401767505', '0.4402096236303', '0.713383838383838', '0.936170212765957', '1', '1', '1'], '1320': ['0.858117326057299', '0.439350525310411', '0.71125', '0.936170212765957', '1', '1', '1'], '1325': ['0.85724043715847', '0.442049808429119', '0.708436724565757', '0.936395759717314', '1', '1', '1'], '1330': ['0.856554564172958', '0.444178246286536', '0.70935960591133', '0.937062937062937', '1', '1', '1'], '1335': ['0.855862068965517', '0.440978886756238', '0.713064713064713', '0.937716262975779', '1', '1', '1'], '1340': ['0.855272226050999', '0.439306358381503', '0.717233009708738', '0.937716262975779', '1', '1', '1'], '1345': ['0.855463347164592', '0.44144578313253', '0.718599033816425', '0.931034482758621', '1', '1', '1'], '1350': ['0.855949895615866', '0.441983630235917', '0.719951923076923', '0.93127147766323', '1', '1', '1'], '1355': ['0.855042016806723', '0.438310129620739', '0.723557692307692', '0.931740614334471', '1', '1', '1'], '1360': ['0.854647099930119', '0.443214629451396', '0.716346153846154', '0.93127147766323', '1', '1', '1'], '1365': ['0.854748603351955', '0.44524843222383', '0.716507177033493', '0.931034482758621', '1', '1', '1'], '1370': ['0.854940434477926', '0.445192307692308', '0.723889555822329', '0.930795847750865', '1', '1', '1'], '1375': ['0.856135401974612', '0.445939452186449', '0.722819593787336', '0.931972789115646', '1', '1', '1'], '1380': ['0.857041755130927', '0.444711538461538', '0.724792408066429', '0.931972789115646', '1', '1', '1'], '1385': ['0.857244318181818', '0.442252165543792', '0.724586288416076', '0.932432432432432', '1', '1', '1'], '1390': ['0.857651245551601', '0.444015444015444', '0.72280701754386', '0.938775510204082', '1', '1', '1'], '1395': ['0.857954545454545', '0.445631067961165', '0.72280701754386', '0.940594059405941', '1', '1', '1'], '1400': ['0.857954545454545', '0.446064139941691', '0.723004694835681', '0.944444444444444', '1', '1', '1'], '1405': ['0.856428571428571', '0.445573294629898', '0.724911452184179', '0.944983818770226', '1', '1', '1'], '1410': ['0.857142857142857', '0.446705426356589', '0.724381625441696', '0.944625407166124', '1', '1', '1'], '1415': ['0.857040229885057', '0.446705426356589', '0.725787631271879', '0.95114006514658', '1', '1', '1'], '1420': ['0.854453294713975', '0.44289156626506', '0.732476635514019', '0.95114006514658', '1', '1', '1'], '1425': ['0.853818181818182', '0.442409638554217', '0.733955659276546', '0.950819672131147', '1', '1', '1'], '1430': ['0.854439592430859', '0.444980694980695', '0.734575087310827', '0.950819672131147', '1', '1', '1'], '1435': ['0.854756717501816', '0.446973365617433', '0.737514518002323', '0.950980392156863', '1', '1', '1'], '1440': ['0.855282199710564', '0.449247207382224', '0.740139211136891', '0.95114006514658', '1', '1', '1'], '1445': ['0.853323699421965', '0.447304516755707', '0.747663551401869', '0.948220064724919', '1', '1', '1'], '1450': ['0.853623188405797', '0.443364122508508', '0.751162790697674', '0.948220064724919', '1', '1', '1'], '1455': ['0.855491329479769', '0.444553004396678', '0.754913294797688', '0.947712418300653', '1', '1', '1'], '1460': ['0.856209150326797', '0.44297601566324', '0.754004576659039', '0.957516339869281', '1', '1', '1'], '1465': ['0.856620336503292', '0.443359375', '0.757403189066059', '0.960526315789474', '1', '1', '1'], '1470': ['0.857142857142857', '0.444227005870842', '0.757094211123723', '0.960912052117264', '1', '1', '1'], '1475': ['0.858504398826979', '0.446297204512016', '0.754246885617214', '0.961165048543689', '1', '1', '1'], '1480': ['0.857875457875458', '0.446191646191646', '0.759637188208617', '0.961538461538462', '1', '1', '1'], '1485': ['0.859765051395007', '0.443298969072165', '0.761363636363636', '0.961165048543689', '1', '1', '1'], '1490': ['0.859985261606485', '0.441986234021632', '0.763513513513513', '0.960912052117264', '1', '1', '1'], '1495': ['0.861131520940485', '0.444938271604938', '0.764044943820225', '0.960912052117264', '1', '1', '1'], '1500': ['0.862426035502959', '0.441379310344828', '0.762276785714286', '0.967320261437908', '1', '1', '1'], '1505': ['0.862962962962963', '0.440394088669951', '0.763128491620112', '0.961038961038961', '1', '1', '1'], '1510': ['0.860326894502229', '0.438856015779093', '0.762276785714286', '0.961538461538462', '1', '1', '1'], '1515': ['0.860014892032763', '0.439108910891089', '0.762222222222222', '0.955696202531646', '1', '1', '1'], '1520': ['0.859806114839672', '0.43858776727996', '0.768976897689769', '0.943396226415094', '1', '1', '1'], '1525': ['0.861940298507463', '0.440298507462687', '0.767364939360529', '0.941358024691358', '1', '1', '1'], '1530': ['0.861733931240658', '0.436381709741551', '0.770419426048565', '0.941176470588235', '1', '1', '1'], '1535': ['0.861630516080778', '0.433681073025335', '0.772626931567329', '0.941176470588235', '1', '1', '1'], '1540': ['0.861573373676248', '0.433943592281049', '0.775330396475771', '0.941896024464832', '1', '1', '1'], '1545': ['0.861678004535147', '0.434739454094293', '0.774229074889868', '0.936555891238671', '1', '1', '1'], '1550': ['0.859101294744859', '0.438396833250866', '0.769315673289183', '0.9375', '1', '1', '1'], '1555': ['0.857794676806084', '0.439424031777557', '0.772026431718062', '0.938053097345133', '1', '1', '1'], '1560': ['0.857467778620167', '0.44344793223717', '0.767876787678768', '0.93841642228739', '1', '1', '1'], '1565': ['0.857575757575757', '0.445164506480558', '0.769570011025358', '0.932551319648094', '1', '1', '1'], '1570': ['0.858562691131498', '0.447761194029851', '0.772777167947311', '0.92463768115942', '1', '1', '1'], '1575': ['0.858570330514988', '0.444942700548082', '0.776572668112798', '0.923529411764706', '1', '1', '1'], '1580': ['0.85945945945946', '0.445273631840796', '0.777535441657579', '0.922190201729106', '1', '1', '1'], '1585': ['0.859581070597362', '0.449304174950298', '0.773913043478261', '0.916184971098266', '1', '1', '1'], '1590': ['0.858585858585859', '0.447761194029851', '0.776330076004343', '0.913544668587896', '1', '1', '1'], '1595': ['0.857476635514019', '0.448430493273543', '0.778741865509761', '0.914285714285714', '1', '1', '1'], '1600': ['0.855919003115265', '0.447052947052947', '0.781148429035753', '0.909090909090909', '1', '1', '1'], '1605': ['0.854150504266874', '0.450025113008538', '0.782327586206897', '0.912429378531073', '1', '1', '1'], '1610': ['0.856259659969088', '0.449898785425101', '0.780409041980624', '0.919667590027701', '1', '1', '1'], '1615': ['0.855384615384615', '0.446830265848671', '0.781914893617021', '0.919889502762431', '1', '1', '1'], '1620': ['0.856589147286822', '0.443367346938776', '0.782377919320594', '0.920765027322404', '1', '1', '1'], '1625': ['0.855702094647013', '0.442062276671771', '0.784877529286475', '0.921195652173913', '1', '1', '1'], '1630': ['0.85480093676815', '0.44365119836818', '0.783669141039236', '0.921621621621622', '1', '1', '1'], '1635': ['0.855355746677092', '0.442857142857143', '0.786016949152542', '0.921832884097035', '1', '1', '1'], '1640': ['0.855678233438486', '0.444670050761421', '0.788297872340426', '0.914438502673797', '1', '1', '1'], '1645': ['0.855450236966825', '0.445685279187817', '0.787234042553192', '0.917553191489362', '1', '1', '1'], '1650': ['0.855784469096672', '0.446310432569975', '0.785638859556494', '0.922666666666667', '1', '1', '1'], '1655': ['0.857482185273159', '0.448416751787538', '0.786540483701367', '0.917989417989418', '1', '1', '1'], '1660': ['0.856235107227959', '0.445696721311475', '0.78816199376947', '0.917333333333333', '1', '1', '1'], '1665': ['0.856687898089172', '0.446666666666667', '0.791752577319588', '0.916890080428954', '1', '1', '1'], '1670': ['0.855084067253803', '0.445579969340828', '0.791925465838509', '0.917771883289125', '1', '1', '1'], '1675': ['0.855645161290322', '0.444330949948927', '0.791537667698658', '0.917771883289125', '1', '1', '1'], '1680': ['0.855761482675262', '0.446437724243977', '0.792607802874743', '0.912698412698413', '1', '1', '1'], '1685': ['0.854368932038835', '0.447462839569452', '0.793422404933196', '0.913385826771654', '1', '1', '1'], '1690': ['0.853559870550162', '0.451282051282051', '0.794238683127572', '0.913612565445026', '1', '1', '1'], '1695': ['0.856219709208401', '0.452258726899384', '0.796086508753862', '0.913612565445026', '1', '1', '1'], '1700': ['0.854251012145749', '0.454126089185033', '0.795454545454545', '0.913838120104439', '1', '1', '1'], '1705': ['0.855177993527508', '0.45482546201232', '0.794818652849741', '0.914285714285714', '1', '1', '1'], '1710': ['0.854707792207792', '0.456320657759507', '0.787784679089027', '0.918158567774936', '1', '1', '1'], '1715': ['0.854353132628153', '0.452772073921971', '0.791925465838509', '0.918367346938775', '1', '1', '1'], '1720': ['0.853518821603928', '0.454871794871795', '0.789038262668046', '0.919191919191919', '1', '1', '1'], '1725': ['0.854337152209493', '0.456041131105398', '0.789907312049434', '0.918987341772152', '1', '1', '1'], '1730': ['0.855973813420622', '0.456420835482207', '0.789907312049434', '0.92', '1', '1', '1'], '1735': ['0.858544562551104', '0.455912863070539', '0.790224032586558', '0.919799498746867', '1', '1', '1'], '1740': ['0.860655737704918', '0.455867082035306', '0.789634146341463', '0.917705735660848', '1', '1', '1'], '1745': ['0.859851607584501', '0.454639709694142', '0.79474216380182', '0.917293233082707', '1', '1', '1'], '1750': ['0.859721082854799', '0.455538221528861', '0.795939086294416', '0.918316831683168', '1', '1', '1'], '1755': ['0.858794384805946', '0.457706279190451', '0.795939086294416', '0.923645320197044', '1', '1', '1'], '1760': ['0.85702479338843', '0.459178367134685', '0.800607287449393', '0.921760391198044', '1', '1', '1'], '1765': ['0.856079404466501', '0.459205020920502', '0.801204819277108', '0.921951219512195', '1', '1', '1'], '1770': ['0.855840927920464', '0.460691823899371', '0.799', '0.921951219512195', '1', '1', '1'], '1775': ['0.853941908713693', '0.463069669984285', '0.803427419354839', '0.91866028708134', '1', '1', '1'], '1780': ['0.85345545378851', '0.463069669984285', '0.80563947633434', '0.91866028708134', '1', '1', '1'], '1785': ['0.8525', '0.461578672242551', '0.805668016194332', '0.921615201900237', '1', '1', '1'], '1790': ['0.850041425020713', '0.468799160985842', '0.803462321792261', '0.922169811320755', '1', '1', '1'], '1795': ['0.850746268656716', '0.473462953231739', '0.803462321792261', '0.922716627634661', '1', '1', '1'], '1800': ['0.851328903654485', '0.472134595162986', '0.804081632653061', '0.923433874709977', '1', '1', '1'], '1805': ['0.849624060150376', '0.47244094488189', '0.80264496439471', '0.923433874709977', '1', '1', '1'], '1810': ['0.848914858096828', '0.469752761704366', '0.804679552390641', '0.928406466512702', '1', '1', '1'], '1815': ['0.848408710217755', '0.471270426989984', '0.804655870445344', '0.928735632183908', '1', '1', '1'], '1820': ['0.850042122999157', '0.472851871375857', '0.803625377643504', '0.929384965831435', '1', '1', '1'], '1825': ['0.851758793969849', '0.479045092838196', '0.801404212637914', '0.929705215419501', '1', '1', '1'], '1830': ['0.852376980817348', '0.47812166488794', '0.804', '0.93018018018018', '1', '1', '1'], '1835': ['0.849498327759197', '0.478609625668449', '0.808191808191808', '0.931111111111111', '1', '1', '1'], '1840': ['0.850083752093802', '0.4784', '0.808853118712274', '0.931718061674009', '1', '1', '1'], '1845': ['0.850847457627119', '0.479872881355932', '0.805443548387097', '0.932166301969365', '1', '1', '1'], '1850': ['0.850467289719626', '0.482010582010582', '0.809716599190283', '0.932608695652174', '1', '1', '1'], '1855': ['0.848976109215017', '0.479365079365079', '0.813197969543147', '0.929184549356223', '1', '1', '1'], '1860': ['0.848588537211292', '0.478880675818374', '0.813265306122449', '0.929637526652452', '1', '1', '1'], '1865': ['0.849656357388316', '0.47626582278481', '0.81734693877551', '0.925373134328358', '1', '1', '1'], '1870': ['0.848667239896819', '0.478306878306878', '0.816243654822335', '0.925531914893617', '1', '1', '1'], '1875': ['0.848588537211292', '0.480891719745223', '0.81910569105691', '0.925373134328358', '1', '1', '1'], '1880': ['0.846022241231822', '0.482446808510638', '0.82020202020202', '0.924406047516199', '1', '1', '1'], '1885': ['0.846022241231822', '0.483750665956313', '0.822222222222222', '0.924568965517241', '1', '1', '1'], '1890': ['0.846219931271478', '0.485380116959064', '0.819838056680162', '0.924568965517241', '1', '1', '1'], '1895': ['0.846153846153846', '0.483580508474576', '0.82370820668693', '0.924892703862661', '1', '1', '1'], '1900': ['0.846153846153846', '0.485138004246284', '0.822695035460993', '0.924892703862661', '1', '1', '1'], '1905': ['0.844234079173838', '0.485607675906183', '0.824186991869919', '0.925690021231423', '1', '1', '1'], '1910': ['0.843053173241852', '0.49063670411985', '0.824365482233503', '0.923728813559322', '1', '1', '1'], '1915': ['0.843642611683849', '0.496518478843064', '0.822515212981744', '0.926160337552743', '1', '1', '1'], '1920': ['0.843373493975904', '0.497851772287863', '0.821572580645161', '0.926160337552743', '1', '1', '1'], '1925': ['0.843103448275862', '0.493787142085359', '0.825174825174825', '0.926470588235294', '1', '1', '1'], '1930': ['0.841968911917098', '0.495934959349593', '0.827860696517413', '0.922594142259414', '1', '1', '1'], '1935': ['0.842287694974003', '0.493210211841391', '0.82970297029703', '0.920335429769392', '1', '1', '1'], '1940': ['0.840909090909091', '0.491883116883117', '0.831849653808111', '0.920335429769392', '1', '1', '1'], '1945': ['0.838454784899034', '0.490249187432286', '0.833333333333333', '0.919491525423729', '1', '1', '1'], '1950': ['0.837885462555066', '0.490238611713666', '0.832681017612524', '0.91578947368421', '1', '1', '1'], '1955': ['0.837312113174182', '0.492690850027071', '0.827317073170732', '0.92600422832981', '1', '1', '1'], '1960': ['0.836879432624114', '0.497025419145484', '0.824337585868499', '0.924843423799583', '1', '1', '1'], '1965': ['0.837789661319073', '0.498920086393089', '0.824509803921569', '0.925465838509317', '1', '1', '1'], '1970': ['0.836007130124777', '0.498378378378378', '0.826129666011788', '0.925925925925926', '1', '1', '1'], '1975': ['0.836752899197145', '0.495661605206074', '0.828125', '0.929896907216495', '1', '1', '1'], '1980': ['0.836752899197145', '0.496735582154516', '0.827016520894072', '0.932098765432099', '1', '1', '1'], '1985': ['0.835874439461883', '0.499185225420967', '0.823929961089494', '0.932238193018481', '1', '1', '1'], '1990': ['0.834977578475336', '0.49945652173913', '0.825365853658536', '0.932377049180328', '1', '1', '1'], '1995': ['0.834080717488789', '0.501633986928105', '0.826171875', '0.93265306122449', '1', '1', '1'], '2000': ['0.83288409703504', '0.500821917808219', '0.826885880077369', '0.932790224032587', '1', '1', '1'], '2005': ['0.833032490974729', '0.504652435686918', '0.825918762088975', '0.933198380566802', '1', '1', '1'], '2010': ['0.832275611967362', '0.507945205479452', '0.82512077294686', '0.933601609657948', '1', '1', '1'], '2015': ['0.834986474301172', '0.510204081632653', '0.825626204238921', '0.929718875502008', '1', '1', '1'], '2020': ['0.834538878842676', '0.508539944903581', '0.824038461538462', '0.9375', '1', '1', '1'], '2025': ['0.836976320582878', '0.508493150684931', '0.825750242013553', '0.93812375249501', '1', '1', '1'], '2030': ['0.835315645013724', '0.512035010940919', '0.82621359223301', '0.936758893280632', '1', '1', '1'], '2035': ['0.835326586936522', '0.510416666666667', '0.827053140096618', '0.9375', '1', '1', '1'], '2040': ['0.835944700460829', '0.512834516657564', '0.82621359223301', '0.940944881889764', '1', '1', '1'], '2045': ['0.835654596100279', '0.509269356597601', '0.83011583011583', '0.940828402366864', '1', '1', '1'], '2050': ['0.836583101207057', '0.507103825136612', '0.833011583011583', '0.945098039215686', '1', '1', '1'], '2055': ['0.835348837209302', '0.505205479452055', '0.833013435700576', '0.946745562130177', '1', '1', '1'], '2060': ['0.835041938490214', '0.506037321624588', '0.830297219558964', '0.950787401574803', '1', '1', '1'], '2065': ['0.833802816901408', '0.510125889436234', '0.82824427480916', '0.954455445544554', '1', '1', '1'], '2070': ['0.832863849765258', '0.512061403508772', '0.830798479087452', '0.95427435387674', '1', '1', '1'], '2075': ['0.830812854442344', '0.514270032930845', '0.827488151658768', '0.954724409448819', '1', '1', '1'], '2080': ['0.830652790917692', '0.513201320132013', '0.827324478178368', '0.955165692007797', '1', '1', '1'], '2085': ['0.830798479087452', '0.515916575192097', '0.824478178368121', '0.95703125', '1', '1', '1'], '2090': ['0.830170777988615', '0.517640573318633', '0.824478178368121', '0.95357833655706', '1', '1', '1'], '2095': ['0.828408007626311', '0.519273127753304', '0.82302568981922', '0.957934990439771', '1', '1', '1'], '2100': ['0.824427480916031', '0.520154610712314', '0.823361823361823', '0.958333333333333', '1', '1', '1'], '2105': ['0.821600771456123', '0.519209659714599', '0.825880114176974', '0.960151802656547', '1', '1', '1'], '2110': ['0.820809248554913', '0.52070679182772', '0.822138126773888', '0.960377358490566', '1', '1', '1'], '2115': ['0.820909970958374', '0.520441988950276', '0.819128787878788', '0.960966542750929', '1', '1', '1'], '2120': ['0.817391304347826', '0.517490283176013', '0.823308270676692', '0.960966542750929', '1', '1', '1'], '2125': ['0.815280464216635', '0.515269294836202', '0.828463713477851', '0.957564575645757', '1', '1', '1'], '2130': ['0.816682832201746', '0.513618677042802', '0.830827067669173', '0.957720588235294', '1', '1', '1'], '2135': ['0.817025440313111', '0.51054384017758', '0.833020637898687', '0.955801104972376', '1', '1', '1'], '2140': ['0.814634146341463', '0.510283490828238', '0.836003770028275', '0.955801104972376', '1', '1', '1'], '2145': ['0.814814814814815', '0.512534818941504', '0.836158192090395', '0.955882352941176', '1', '1', '1'], '2150': ['0.815968841285297', '0.512849162011173', '0.834430856067733', '0.956043956043956', '1', '1', '1'], '2155': ['0.812256809338521', '0.514301738642737', '0.834896810506567', '0.956284153005464', '1', '1', '1'], '2160': ['0.812316715542522', '0.516835016835017', '0.836295603367633', '0.954710144927536', '1', '1', '1'], '2165': ['0.81041257367387', '0.516545148625911', '0.834733893557423', '0.954710144927536', '1', '1', '1'], '2170': ['0.81163708086785', '0.516778523489933', '0.834888059701492', '0.953959484346225', '1', '1', '1'], '2175': ['0.814925373134328', '0.514779698828779', '0.837686567164179', '0.950367647058823', '1', '1', '1'], '2180': ['0.814667988107037', '0.518518518518518', '0.837962962962963', '0.950184501845019', '1', '1', '1'], '2185': ['0.812685827552032', '0.52049410443571', '0.837662337662338', '0.95045871559633', '1', '1', '1'], '2190': ['0.814484126984127', '0.520786516853933', '0.836279069767442', '0.950729927007299', '1', '1', '1'], '2195': ['0.817547357926221', '0.523033707865169', '0.832402234636871', '0.951086956521739', '1', '1', '1'], '2200': ['0.817910447761194', '0.528981429375352', '0.830697674418605', '0.954873646209386', '1', '1', '1'], '2205': ['0.816733067729084', '0.530669667979741', '0.832089552238806', '0.954873646209386', '1', '1', '1'], '2210': ['0.815', '0.525155455059356', '0.83364312267658', '0.955357142857143', '1', '1', '1'], '2215': ['0.814629258517034', '0.527746319365798', '0.832252085264133', '0.959074733096085', '1', '1', '1'], '2220': ['0.813', '0.527003979533826', '0.833178869323448', '0.961267605633803', '1', '1', '1'], '2225': ['0.811811811811812', '0.524431818181818', '0.832096474953618', '0.962633451957295', '1', '1', '1'], '2230': ['0.811931243680485', '0.523702031602709', '0.834264432029795', '0.962765957446809', '1', '1', '1'], '2235': ['0.81237322515213', '0.52056338028169', '0.835041938490214', '0.964476021314387', '1', '1', '1'], '2240': ['0.813074565883555', '0.519955030916245', '0.836431226765799', '0.964285714285714', '1', '1', '1'], '2245': ['0.815843621399177', '0.523223279238948', '0.837686567164179', '0.964285714285714', '1', '1', '1'], '2250': ['0.815843621399177', '0.526521496370743', '0.836772983114446', '0.9644128113879', '1', '1', '1'], '2255': ['0.813977389516958', '0.52436974789916', '0.834905660377359', '0.965034965034965', '1', '1', '1'], '2260': ['0.812564366632338', '0.529708520179372', '0.833958724202627', '0.966549295774648', '1', '1', '1'], '2265': ['0.815082644628099', '0.529708520179372', '0.833020637898687', '0.966490299823633', '1', '1', '1'], '2270': ['0.815925542916236', '0.53105763850028', '0.833805476864967', '0.966666666666667', '1', '1', '1'], '2275': ['0.815925542916236', '0.532994923857868', '0.830524344569288', '0.968586387434555', '1', '1', '1'], '2280': ['0.817713697219361', '0.534726143421796', '0.829107981220657', '0.968641114982578', '1', '1', '1'], '2285': ['0.816973415132924', '0.538636363636364', '0.830540037243948', '0.971731448763251', '1', '1', '1'], '2290': ['0.817718940936864', '0.537449971412236', '0.832252085264133', '0.971631205673759', '1', '1', '1'], '2295': ['0.816973415132924', '0.53824200913242', '0.835348837209302', '0.971731448763251', '1', '1', '1'], '2300': ['0.816326530612245', '0.540757749712974', '0.832252085264133', '0.97153024911032', '1', '1', '1'], '2305': ['0.815843621399177', '0.542237442922374', '0.835195530726257', '0.96969696969697', '1', '1', '1'], '2310': ['0.817248459958932', '0.5446735395189', '0.838139534883721', '0.971479500891265', '1', '1', '1'], '2315': ['0.817248459958932', '0.545871559633028', '0.840633737185461', '0.971479500891265', '1', '1', '1'], '2320': ['0.814624098867147', '0.545558739255014', '0.841417910447761', '0.97158081705151', '1', '1', '1'], '2325': ['0.812177502579979', '0.545714285714286', '0.845864661654135', '0.968197879858657', '1', '1', '1'], '2330': ['0.812371134020619', '0.548479632816982', '0.840972871842844', '0.971631205673759', '1', '1', '1'], '2335': ['0.814049586776859', '0.552178899082569', '0.842549203373946', '0.968197879858657', '1', '1', '1'], '2340': ['0.811458333333333', '0.552238805970149', '0.84171322160149', '0.968253968253968', '1', '1', '1'], '2345': ['0.812304483837331', '0.553191489361702', '0.841078066914498', '0.9701230228471', '1', '1', '1'], '2350': ['0.810272536687631', '0.553581661891117', '0.842300556586271', '0.969804618117229', '1', '1', '1'], '2355': ['0.809623430962343', '0.557471264367816', '0.842883548983364', '0.969642857142857', '1', '1', '1'], '2360': ['0.810020876826722', '0.552479815455594', '0.846153846153846', '0.966608084358524', '1', '1', '1'], '2365': ['0.808176100628931', '0.552540415704388', '0.846296296296296', '0.966898954703833', '1', '1', '1'], '2370': ['0.808622502628812', '0.553571428571429', '0.846225535880708', '0.967241379310345', '1', '1', '1'], '2375': ['0.807570977917981', '0.551963048498845', '0.84794776119403', '0.967409948542024', '1', '1', '1'], '2380': ['0.806485355648536', '0.554782608695652', '0.844939647168059', '0.974182444061962', '1', '1', '1'], '2385': ['0.80651945320715', '0.556199304750869', '0.843720930232558', '0.974402730375427', '1', '1', '1'], '2390': ['0.804852320675106', '0.555877243775333', '0.845724907063197', '0.974315068493151', '1', '1', '1'], '2395': ['0.805263157894737', '0.558260869565217', '0.845650140318054', '0.974533106960951', '1', '1', '1'], '2400': ['0.803571428571429', '0.560791157649796', '0.846728971962617', '0.974533106960951', '1', '1', '1'], '2405': ['0.803571428571429', '0.560791157649796', '0.846728971962617', '0.974533106960951', '1', '1', '1'], '2410': ['0.803364879074658', '0.562209302325581', '0.850187265917603', '0.967851099830795', '1', '1', '1'], '2415': ['0.804439746300211', '0.560394889663182', '0.848598130841121', '0.971283783783784', '1', '1', '1'], '2420': ['0.80338266384778', '0.564712710388857', '0.846728971962617', '0.974619289340101', '1', '1', '1'], '2425': ['0.804670912951168', '0.564991334488735', '0.846948356807512', '0.974662162162162', '1', '1', '1'], '2430': ['0.805763073639274', '0.5625', '0.842990654205607', '0.978077571669477', '1', '1', '1'], '2435': ['0.804878048780488', '0.562463683904707', '0.844216417910448', '0.978040540540541', '1', '1', '1'], '2440': ['0.801058201058201', '0.563191613278975', '0.844714686623012', '0.978187919463087', '1', '1', '1'], '2445': ['0.79746835443038', '0.565420560747664', '0.843137254901961', '0.978151260504202', '1', '1', '1'], '2450': ['0.796394485683987', '0.562902282036279', '0.844651162790698', '0.97822445561139', '1', '1', '1'], '2455': ['0.795309168443497', '0.561659848042081', '0.852198316183349', '0.975206611570248', '1', '1', '1'], '2460': ['0.795309168443497', '0.56173200702165', '0.852443609022556', '0.975409836065574', '1', '1', '1'], '2465': ['0.792993630573248', '0.564885496183206', '0.854990583804143', '0.975450081833061', '1', '1', '1'], '2470': ['0.792993630573248', '0.563861094761625', '0.857142857142857', '0.975450081833061', '1', '1', '1'], '2475': ['0.792194092827004', '0.564525633470831', '0.861873226111637', '0.975530179445351', '1', '1', '1'], '2480': ['0.791359325605901', '0.563571850975754', '0.863039399624766', '0.975288303130148', '1', '1', '1'], '2485': ['0.791754756871036', '0.564754583086931', '0.864104967197751', '0.978653530377668', '1', '1', '1'], '2490': ['0.790870488322718', '0.564754583086931', '0.861842105263158', '0.978827361563518', '1', '1', '1'], '2495': ['0.790149892933619', '0.56570418385386', '0.861971830985915', '0.978792822185971', '1', '1', '1'], '2500': ['0.79144385026738', '0.565525383707202', '0.864661654135338', '0.980456026058632', '1', '1', '1'], '2505': ['0.790374331550802', '0.567871962062833', '0.865671641791045', '0.980263157894737', '1', '1', '1'], '2510': ['0.789137380191693', '0.572532699167658', '0.865168539325843', '0.980295566502463', '1', '1', '1'], '2515': ['0.787846481876333', '0.570917759237187', '0.865294667913938', '0.980295566502463', '1', '1', '1'], '2520': ['0.784877529286475', '0.57501494321578', '0.865671641791045', '0.98019801980198', '1', '1', '1'], '2525': ['0.781818181818182', '0.575775656324582', '0.865546218487395', '0.980230642504119', '1', '1', '1'], '2530': ['0.781350482315113', '0.577817531305903', '0.864738805970149', '0.980230642504119', '1', '1', '1'], '2535': ['0.779806659505908', '0.579572446555819', '0.864534336782691', '0.980327868852459', '1', '1', '1'], '2540': ['0.781350482315113', '0.578134284016637', '0.866981132075472', '0.980360065466448', '1', '1', '1'], '2545': ['0.78051391862955', '0.578478002378121', '0.866477272727273', '0.980360065466448', '1', '1', '1'], '2550': ['0.777540106951872', '0.57910447761194', '0.868421052631579', '0.980230642504119', '1', '1', '1'], '2555': ['0.776357827476038', '0.579231692677071', '0.87066541705717', '0.980230642504119', '1', '1', '1'], '2560': ['0.777070063694268', '0.580120481927711', '0.868667917448405', '0.983633387888707', '1', '1', '1'], '2565': ['0.775661375661376', '0.582577132486388', '0.867729831144465', '0.9836867862969', '1', '1', '1'], '2570': ['0.770700636942675', '0.585748792270531', '0.865475070555033', '0.98371335504886', '1', '1', '1'], '2575': ['0.768331562167906', '0.589264173703257', '0.867674858223062', '0.983739837398374', '1', '1', '1'], '2580': ['0.763771186440678', '0.592749244712991', '0.867172675521822', '0.983870967741935', '1', '1', '1'], '2585': ['0.765208110992529', '0.592904389657246', '0.866284622731614', '0.982428115015975', '1', '1', '1'], '2590': ['0.76307363927428', '0.594708358388455', '0.86673058485139', '0.9808', '1', '1', '1'], '2595': ['0.762460233297985', '0.598791540785498', '0.866346153846154', '0.9808', '1', '1', '1'], '2600': ['0.763771186440678', '0.599027946537059', '0.868068833652008', '0.9808', '1', '1', '1'], '2605': ['0.762962962962963', '0.59718826405868', '0.866156787762906', '0.980861244019139', '1', '1', '1'], '2610': ['0.764270613107822', '0.595340282035561', '0.866666666666667', '0.980769230769231', '1', '1', '1'], '2615': ['0.76215644820296', '0.595953402820356', '0.867745004757374', '0.9808', '1', '1', '1'], '2620': ['0.762355415352261', '0.598894348894349', '0.868320610687023', '0.9808', '1', '1', '1'], '2625': ['0.761052631578947', '0.599632127529123', '0.868899521531101', '0.980830670926517', '1', '1', '1'], '2630': ['0.762105263157895', '0.601596071209331', '0.873804971319312', '0.980891719745223', '1', '1', '1'], '2635': ['0.763350785340314', '0.604938271604938', '0.873574144486692', '0.980769230769231', '1', '1', '1'], '2640': ['0.763541666666667', '0.604593420235878', '0.877840909090909', '0.980645161290322', '1', '1', '1'], '2645': ['0.762303664921466', '0.604708798017348', '0.878672985781991', '0.980707395498392', '1', '1', '1'], '2650': ['0.762658227848101', '0.602722772277228', '0.880188679245283', '0.979166666666667', '1', '1', '1'], '2655': ['0.759493670886076', '0.602230483271376', '0.884578997161779', '0.97933227344992', '1', '1', '1'], '2660': ['0.762105263157895', '0.602722772277228', '0.887939221272555', '0.979299363057325', '1', '1', '1'], '2665': ['0.761399787910923', '0.600370599135269', '0.891098484848485', '0.980891719745223', '1', '1', '1'], '2670': ['0.759533898305085', '0.602342786683107', '0.889523809523809', '0.982539682539682', '1', '1', '1'], '2675': ['0.759574468085106', '0.603321033210332', '0.890267175572519', '0.982456140350877', '1', '1', '1'], '2680': ['0.759023354564756', '0.602823818293432', '0.89261744966443', '0.982428115015975', '1', '1', '1'], '2685': ['0.759533898305085', '0.607734806629834', '0.892204042348412', '0.982484076433121', '1', '1', '1'], '2690': ['0.760800842992624', '0.607493857493858', '0.895551257253385', '0.982539682539682', '1', '1', '1'], '2695': ['0.758149316508938', '0.605166051660517', '0.897386253630203', '0.98256735340729', '1', '1', '1'], '2700': ['0.756046267087277', '0.609741060419236', '0.894685990338164', '0.982649842271293', '1', '1', '1'], '2705': ['0.755252100840336', '0.608776266996292', '0.895752895752896', '0.982649842271293', '1', '1', '1'], '2710': ['0.753943217665615', '0.612484548825711', '0.896917148362235', '0.98256735340729', '1', '1', '1'], '2715': ['0.753699788583509', '0.6134401972873', '0.896718146718147', '0.980982567353407', '1', '1', '1'], '2720': ['0.75210970464135', '0.621905940594059', '0.895292987512008', '0.977671451355662', '1', '1', '1'], '2725': ['0.752642706131078', '0.620347394540943', '0.896452540747843', '0.976152623211447', '1', '1', '1'], '2730': ['0.751585623678647', '0.620261031696706', '0.895693779904306', '0.977883096366509', '1', '1', '1'], '2735': ['0.750791974656811', '0.620324189526184', '0.897142857142857', '0.977742448330683', '1', '1', '1'], '2740': ['0.751054852320675', '0.616770186335404', '0.903753609239653', '0.977742448330683', '1', '1', '1'], '2745': ['0.747863247863248', '0.61495673671199', '0.908133971291866', '0.9776', '1', '1', '1'], '2750': ['0.745980707395498', '0.6168108776267', '0.91030534351145', '0.977491961414791', '1', '1', '1'], '2755': ['0.745435016111708', '0.61495673671199', '0.913085004775549', '0.97752808988764', '1', '1', '1'], '2760': ['0.748387096774194', '0.614100185528757', '0.911089866156788', '0.977671451355662', '1', '1', '1'], '2765': ['0.748651564185545', '0.612723903644225', '0.911259541984733', '0.977564102564103', '1', '1', '1'], '2770': ['0.750812567713976', '0.6134401972873', '0.91395793499044', '0.9776', '1', '1', '1'], '2775': ['0.749729144095341', '0.61628624305984', '0.911792905081496', '0.9776', '1', '1', '1'], '2780': ['0.746187363834423', '0.616', '0.911792905081496', '0.9776', '1', '1', '1'], '2785': ['0.742702702702703', '0.619047619047619', '0.910047846889952', '0.979166666666667', '1', '1', '1'], '2790': ['0.739978331527627', '0.621221468229488', '0.90978886756238', '0.979166666666667', '1', '1', '1'], '2795': ['0.738276990185387', '0.623312883435583', '0.909353905496625', '0.9792', '1', '1', '1'], '2800': ['0.737417943107221', '0.626225490196078', '0.907066795740561', '0.982456140350877', '1', '1', '1'], '2805': ['0.736842105263158', '0.626225490196078', '0.906796116504854', '0.982539682539682', '1', '1', '1'], '2810': ['0.733186328555678', '0.629130966952264', '0.906886517943744', '0.982539682539682', '1', '1', '1'], '2815': ['0.736725663716814', '0.627522935779817', '0.909796314258002', '0.982511923688394', '1', '1', '1'], '2820': ['0.735911602209945', '0.628220858895706', '0.908212560386473', '0.9856', '1', '1', '1'], '2825': ['0.735973597359736', '0.63193588162762', '0.908477842003854', '0.985623003194888', '1', '1', '1'], '2830': ['0.735973597359736', '0.634071340713407', '0.911650485436893', '0.9856', '1', '1', '1'], '2835': ['0.734939759036145', '0.636812847436689', '0.910592808551992', '0.985645933014354', '1', '1', '1'], '2840': ['0.73047304730473', '0.639213275968039', '0.911851126346719', '0.985714285714286', '1', '1', '1'], '2845': ['0.732673267326733', '0.638546798029557', '0.912915851272016', '0.984177215189873', '1', '1', '1'], '2850': ['0.730684326710817', '0.640394088669951', '0.9130859375', '0.984152139461173', '1', '1', '1'], '2855': ['0.725966850828729', '0.644307692307692', '0.912487708947886', '0.984301412872842', '1', '1', '1'], '2860': ['0.724366041896362', '0.647058823529412', '0.910521140609636', '0.984423676012461', '1', '1', '1'], '2865': ['0.722160970231532', '0.649101053936764', '0.91078431372549', '0.984350547730829', '1', '1', '1'], '2870': ['0.721672167216722', '0.650310559006211', '0.91078431372549', '0.984227129337539', '1', '1', '1'], '2875': ['0.722587719298246', '0.650062266500623', '0.909448818897638', '0.984276729559748', '1', '1', '1'], '2880': ['0.722466960352423', '0.653150343106675', '0.909090909090909', '0.984251968503937', '1', '1', '1'], '2885': ['0.723872387238724', '0.6525', '0.914230019493177', '0.984202211690363', '1', '1', '1'], '2890': ['0.725576289791438', '0.654934003771213', '0.913926499032882', '0.985714285714286', '1', '1', '1'], '2895': ['0.725770925110132', '0.656171284634761', '0.912162162162162', '0.985759493670886', '1', '1', '1'], '2900': ['0.72142064372919', '0.655562539283469', '0.914175506268081', '0.985781990521327', '1', '1', '1'], '2905': ['0.720441988950276', '0.655520504731861', '0.916023166023166', '0.985871271585557', '1', '1', '1'], '2910': ['0.717892425905598', '0.65991133628879', '0.913759689922481', '0.987480438184664', '1', '1', '1'], '2915': ['0.715536105032823', '0.66010165184244', '0.91674733785092', '0.987441130298273', '1', '1', '1'], '2920': ['0.716157205240175', '0.664540816326531', '0.916023166023166', '0.9875', '1', '1', '1'], '2925': ['0.714912280701754', '0.666029318036966', '0.918111753371869', '0.987460815047022', '1', '1', '1'], '2930': ['0.714599341383096', '0.670505438259757', '0.919540229885057', '0.987460815047022', '1', '1', '1'], '2935': ['0.713656387665198', '0.670498084291188', '0.922264875239923', '0.987480438184664', '1', '1', '1'], '2940': ['0.712719298245614', '0.673926969891095', '0.922854387656702', '0.987577639751553', '1', '1', '1'], '2945': ['0.710526315789474', '0.673745173745174', '0.923444976076555', '0.987538940809969', '1', '1', '1'], '2950': ['0.709110867178924', '0.675449871465296', '0.923076923076923', '0.989147286821705', '1', '1', '1'], '2955': ['0.707692307692308', '0.675257731958763', '0.923444976076555', '0.989130434782609', '1', '1', '1'], '2960': ['0.709289617486339', '0.679586563307494', '0.924783027965284', '0.989247311827957', '1', '1', '1'], '2965': ['0.708971553610503', '0.67808661926309', '0.925747348119576', '0.99079754601227', '1', '1', '1'], '2970': ['0.707742639040349', '0.680051813471503', '0.927675988428158', '0.990769230769231', '1', '1', '1'], '2975': ['0.707290533188248', '0.683084899546338', '0.927395934172314', '0.99079754601227', '1', '1', '1'], '2980': ['0.706971677559913', '0.684142394822006', '0.93002915451895', '0.990825688073394', '1', '1', '1'], '2985': ['0.70620239390642', '0.689206762028608', '0.926285160038797', '0.992401215805471', '1', '1', '1'], '2990': ['0.703344120819849', '0.690849673202614', '0.926356589147287', '0.992389649923896', '1', '1', '1'], '2995': ['0.703344120819849', '0.692357935989549', '0.926141885325559', '0.992401215805471', '1', '1', '1'], '3000': ['0.703260869565217', '0.69355888093689', '0.924198250728863', '0.992389649923896', '1', '1', '1'], '3005': ['0.701298701298701', '0.695822454308094', '0.924271844660194', '0.992343032159265', '1', '1', '1'], '3010': ['0.698051948051948', '0.697187704381949', '0.926499032882012', '0.992331288343558', '1', '1', '1'], '3015': ['0.7', '0.699737187910644', '0.928085519922255', '0.992343032159265', '1', '1', '1'], '3020': ['0.694896851248643', '0.701502286087525', '0.928085519922255', '0.992331288343558', '1', '1', '1'], '3025': ['0.691384950926936', '0.701891715590346', '0.929194956353055', '0.993855606758832', '1', '1', '1'], '3030': ['0.690631808278867', '0.701891715590346', '0.933658536585366', '0.993893129770992', '1', '1', '1'], '3035': ['0.686746987951807', '0.703246753246753', '0.933202357563851', '0.993939393939394', '1', '1', '1'], '3040': ['0.684901531728665', '0.707221860767729', '0.934313725490196', '0.993948562783661', '1', '1', '1'], '3045': ['0.683168316831683', '0.706840390879479', '0.936647173489279', '0.993930197268589', '1', '1', '1'], '3050': ['0.682872928176796', '0.709824333116461', '0.93579766536965', '0.993865030674847', '1', '1', '1'], '3055': ['0.681718061674009', '0.709424083769633', '0.936293436293436', '0.993808049535604', '1', '1', '1'], '3060': ['0.681367144432194', '0.711475409836066', '0.936538461538462', '0.993808049535604', '1', '1', '1'], '3065': ['0.678492239467849', '0.714751958224543', '0.936416184971098', '0.993779160186625', '1', '1', '1'], '3070': ['0.675946547884187', '0.716330513988289', '0.936354869816779', '0.996889580093313', '1', '1', '1'], '3075': ['0.675946547884187', '0.717079530638853', '0.936293436293436', '0.996899224806202', '1', '1', '1'], '3080': ['0.674496644295302', '0.721354166666667', '0.936599423631124', '0.996884735202492', '1', '1', '1'], '3085': ['0.673743016759777', '0.721932114882507', '0.937560038424592', '0.996894409937888', '1', '1', '1'], '3090': ['0.672645739910314', '0.72265625', '0.939071566731141', '0.996913580246913', '1', '1', '1'], '3095': ['0.670416197975253', '0.722727272727273', '0.939189189189189', '0.996870109546166', '1', '1', '1'], '3100': ['0.669662921348315', '0.726445743989604', '0.940096618357488', '0.996840442338073', '1', '1', '1'], '3105': ['0.670428893905192', '0.725324675324675', '0.940269749518304', '0.996825396825397', '1', '1', '1'], '3110': ['0.670828603859251', '0.72809863724854', '0.938342967244701', '0.996835443037975', '1', '1', '1'], '3115': ['0.668949771689498', '0.727860374919198', '0.939805825242718', '0.996870109546166', '1', '1', '1'], '3120': ['0.668941979522184', '0.731168831168831', '0.939864209505335', '0.996899224806202', '1', '1', '1'], '3125': ['0.668558456299659', '0.734587929915639', '0.941634241245136', '0.996889580093313', '1', '1', '1'], '3130': ['0.667042889390519', '0.738219895287958', '0.941860465116279', '0.996899224806202', '1', '1', '1'], '3135': ['0.665163472378805', '0.73915900131406', '0.94294003868472', '0.996908809891808', '1', '1', '1'], '3140': ['0.662514156285391', '0.738845144356955', '0.942884801548887', '0.996904024767802', '1', '1', '1'], '3145': ['0.659090909090909', '0.741808650065531', '0.94294003868472', '0.996899224806202', '1', '1', '1'], '3150': ['0.656784492588369', '0.743774574049803', '0.943105110896818', '0.996904024767802', '1', '1', '1'], '3155': ['0.654816513761468', '0.744277305428385', '0.943159922928709', '0.996879875195008', '1', '1', '1'], '3160': ['0.653624856156502', '0.748206131767776', '0.943961352657005', '0.996894409937888', '1', '1', '1'], '3165': ['0.650630011454754', '0.75065445026178', '0.9450337512054', '0.996894409937888', '1', '1', '1'], '3170': ['0.649885583524027', '0.75344262295082', '0.945139557266602', '0.996889580093313', '1', '1', '1'], '3175': ['0.647326507394767', '0.76149802890933', '0.945788964181994', '0.996908809891808', '1', '1', '1'], '3180': ['0.646924829157175', '0.763624425476034', '0.946601941747573', '0.996908809891808', '1', '1', '1'], '3185': ['0.643020594965675', '0.765706806282722', '0.947470817120622', '0.998459167950693', '1', '1', '1'], '3190': ['0.641466208476518', '0.766666666666667', '0.949069539666993', '0.998463901689708', '1', '1', '1'], '3195': ['0.639269406392694', '0.768372703412074', '0.950048971596474', '0.998461538461538', '1', '1', '1'], '3200': ['0.636467889908257', '0.769180327868853', '0.95219512195122', '0.998454404945904', '1', '1', '1'], '3205': ['0.635321100917431', '0.767564018384767', '0.955252918287938', '0.998447204968944', '1', '1', '1'], '3210': ['0.63302752293578', '0.770545693622617', '0.95618305744888', '0.998449612403101', '1', '1', '1'], '3215': ['0.632183908045977', '0.767303889255109', '0.958333333333333', '0.998449612403101', '1', '1', '1'], '3220': ['0.629200463499421', '0.76983606557377', '0.958292919495635', '0.998439937597504', '1', '1', '1'], '3225': ['0.626744186046512', '0.771447282252783', '0.959302325581395', '0.9984375', '1', '1', '1'], '3230': ['0.623255813953488', '0.774214659685864', '0.960309777347531', '0.998422712933754', '1', '1', '1'], '3235': ['0.625581395348837', '0.77391874180865', '0.961352657004831', '1', '1', '1', '1'], '3240': ['0.624854819976771', '0.775081967213115', '0.962209302325581', '1', '1', '1', '1'], '3245': ['0.625724217844728', '0.775443204202232', '0.963213939980639', '1', '1', '1', '1'], '3250': ['0.623693379790941', '0.778215223097113', '0.9642166344294', '1', '1', '1', '1'], '3255': ['0.622969837587007', '0.780632411067194', '0.964388835418672', '1', '1', '1', '1'], '3260': ['0.624129930394432', '0.781806196440343', '0.965384615384615', '1', '1', '1', '1'], '3265': ['0.624854819976771', '0.781002638522427', '0.965217391304348', '1', '1', '1', '1'], '3270': ['0.622222222222222', '0.780407626561473', '0.965217391304348', '1', '1', '1', '1'], '3275': ['0.618203309692671', '0.781188765512737', '0.964181994191675', '1', '1', '1', '1'], '3280': ['0.617751479289941', '0.781699346405229', '0.965082444228904', '1', '1', '1', '1'], '3285': ['0.617577197149644', '0.779882429784455', '0.965250965250965', '1', '1', '1', '1'], '3290': ['0.615017878426698', '0.780456026058632', '0.966150870406189', '1', '1', '1', '1'], '3295': ['0.613365155131265', '0.782184655396619', '0.967149758454106', '1', '1', '1', '1'], '3300': ['0.610778443113772', '0.783398184176394', '0.968085106382979', '0.998397435897436', '1', '1', '1'], '3305': ['0.610108303249097', '0.784466019417476', '0.967898832684825', '0.998410174880763', '1', '1', '1'], '3310': ['0.612709832134293', '0.786085825747724', '0.969082125603865', '0.998397435897436', '1', '1', '1'], '3315': ['0.611778846153846', '0.786269430051813', '0.971789883268482', '0.998392282958199', '1', '1', '1'], '3320': ['0.613173652694611', '0.788586251621271', '0.971734892787524', '0.998392282958199', '1', '1', '1'], '3325': ['0.615017878426698', '0.789199739752765', '0.970760233918129', '1', '1', '1', '1'], '3330': ['0.614832535885167', '0.790637191157347', '0.973709834469328', '1', '1', '1', '1'], '3335': ['0.611510791366906', '0.794671864847303', '0.973658536585366', '1', '1', '1', '1'], '3340': ['0.610047846889952', '0.795705920624593', '0.9736328125', '1', '1', '1', '1'], '3345': ['0.607913669064748', '0.799610894941634', '0.973529411764706', '1', '1', '1', '1'], '3350': ['0.607185628742515', '0.800388852883992', '0.973451327433628', '1', '1', '1', '1'], '3355': ['0.607185628742515', '0.801685029163966', '0.973372781065089', '1', '1', '1', '1'], '3360': ['0.601907032181168', '0.807040417209909', '0.973477406679764', '1', '1', '1', '1'], '3365': ['0.598086124401914', '0.804941482444733', '0.975272007912957', '1', '1', '1', '1'], '3370': ['0.59375', '0.804277381723914', '0.979125248508946', '1', '1', '1', '1'], '3375': ['0.592326139088729', '0.8046875', '0.981150793650794', '1', '1', '1', '1'], '3380': ['0.590909090909091', '0.802743305029392', '0.983050847457627', '1', '1', '1', '1'], '3385': ['0.592105263157895', '0.804830287206266', '0.983084577114428', '1', '1', '1', '1'], '3390': ['0.589712918660287', '0.805609915198956', '0.986013986013986', '1', '1', '1', '1'], '3395': ['0.589285714285714', '0.806810740013098', '0.988955823293173', '1', '1', '1', '1'], '3400': ['0.585918854415275', '0.808371484630477', '0.988888888888889', '1', '1', '1', '1'], '3405': ['0.583333333333333', '0.812704649639817', '0.988843813387424', '1', '1', '1', '1'], '3410': ['0.582142857142857', '0.815686274509804', '0.989785495403473', '1', '1', '1', '1'], '3415': ['0.58183990442055', '0.814983713355049', '0.990769230769231', '1', '1', '1', '1'], '3420': ['0.578384798099763', '0.819790301441678', '0.990750256937307', '1', '1', '1', '1'], '3425': ['0.574821852731591', '0.824262295081967', '0.990740740740741', '1', '1', '1', '1'], '3430': ['0.574468085106383', '0.830151415404872', '0.990712074303405', '1', '1', '1', '1'], '3435': ['0.570405727923628', '0.830287206266319', '0.990644490644491', '1', '1', '1', '1'], '3440': ['0.562425683709869', '0.835409836065574', '0.989594172736732', '1', '1', '1', '1'], '3445': ['0.561236623067776', '0.835301837270341', '0.990556138509968', '1', '1', '1', '1'], '3450': ['0.557416267942584', '0.837908496732026', '0.990466101694915', '1', '1', '1', '1'], '3455': ['0.555288461538462', '0.8382257012394', '0.990445859872611', '1', '1', '1', '1'], '3460': ['0.554621848739496', '0.841280209013716', '0.990384615384615', '1', '1', '1', '1'], '3465': ['0.553699284009547', '0.846153846153846', '0.990425531914894', '1', '1', '1', '1'], '3470': ['0.551435406698565', '0.847568988173456', '0.99144385026738', '1', '1', '1', '1'], '3475': ['0.549700598802395', '0.848944591029024', '0.991462113127001', '1', '1', '1', '1'], '3480': ['0.54653937947494', '0.852902374670185', '0.991341991341991', '1', '1', '1', '1'], '3485': ['0.542959427207637', '0.854689564068692', '0.991323210412148', '1', '1', '1', '1'], '3490': ['0.539379474940334', '0.856481481481482', '0.993456924754635', '1', '1', '1', '1'], '3495': ['0.537544696066746', '0.860541969596827', '0.993406593406593', '1', '1', '1', '1'], '3500': ['0.535799522673031', '0.86234281932495', '0.99552071668533', '1', '1', '1', '1'], '3505': ['0.533492822966507', '0.863059452237809', '0.995525727069351', '1', '1', '1', '1'], '3510': ['0.531736526946108', '0.870320855614973', '0.995449374288965', '1', '1', '1', '1'], '3515': ['0.52757793764988', '0.873324396782842', '0.997716894977169', '1', '1', '1', '1'], '3520': ['0.524433849821216', '0.880677966101695', '0.997716894977169', '1', '1', '1', '1'], '3525': ['0.51961950059453', '0.884562841530055', '0.997716894977169', '1', '1', '1', '1'], '3530': ['0.519002375296912', '0.886648122392211', '0.998870056497175', '1', '1', '1', '1'], '3535': ['0.518256772673734', '0.892025405786874', '0.998857142857143', '1', '1', '1', '1'], '3540': ['0.515789473684211', '0.896848137535817', '0.998864926220204', '1', '1', '1', '1'], '3545': ['0.51219512195122', '0.903438185808339', '0.998877665544332', '1', '1', '1', '1'], '3550': ['0.509259259259259', '0.911111111111111', '0.998873873873874', '1', '1', '1', '1'], '3555': ['0.502870264064294', '0.916666666666667', '1', '1', '1', '1', '1'], '3560': ['0.492622020431328', '0.926848249027237', '1', '1', '1', '1', '1'], '3565': ['0.488188976377953', '0.935846030473135', '1', '1', '1', '1', '1'], '3570': ['0.48494983277592', '0.946764946764947', '1', '1', '1', '1', '1'], '3575': ['0.482300884955752', '0.953508030431107', '1', '1', '1', '1', '1'], '3580': ['0.479825517993457', '0.967013888888889', '1', '1', '1', '1', '1'], '3585': ['0.477595628415301', '0.968861209964413', '1', '1', '1', '1', '1'], '3590': ['0.475622968580715', '0.984417965169569', '1', '1', '1', '1', '1'], '3595': ['0.469255663430421', '0.993408662900188', '1', '1', '1', '1', '1'], '3600': ['0.463282937365011', '1', '1', '1', '1', '1', '1'], '3605': ['0.463282937365011', '0', '0', '0', '0', '0', '0'], '3610': ['0.462702702702703', '1', '0', '0', '0', '0', '0'], '3615': ['0.459194776931447', '1', '0', '0', '0', '0', '0'], '3620': ['0.453846153846154', '1', '0', '0', '0', '0', '0'], '3625': ['0.446547884187082', '1', '0', '0', '0', '0', '0'], '3630': ['0.442199775533109', '1', '0', '0', '0', '0', '0'], '3635': ['0.439051918735892', '1', '0', '0', '0', '0', '0'], '3640': ['0.438418079096045', '1', '0', '0', '0', '0', '0'], '3645': ['0.437146092865232', '1', '0', '0', '0', '0', '0'], '3650': ['0.434584755403868', '1', '0', '0', '0', '0', '0'], '3655': ['0.425433526011561', '1', '0', '0', '0', '0', '0'], '3660': ['0.422093023255814', '1', '0', '0', '0', '0', '0'], '3665': ['0.419392523364486', '1', '0', '0', '0', '0', '0'], '3670': ['0.412529550827423', '1', '0', '0', '0', '0', '0'], '3675': ['0.409738717339667', '1', '0', '0', '0', '0', '0'], '3680': ['0.405502392344498', '1', '0', '0', '0', '0', '0'], '3685': ['0.399032648125756', '1', '0', '0', '0', '0', '0'], '3690': ['0.396111786148238', '1', '0', '0', '0', '0', '0'], '3695': ['0.393162393162393', '1', '0', '0', '0', '0', '0'], '3700': ['0.38641975308642', '1', '0', '0', '0', '0', '0'], '3705': ['0.38107098381071', '1', '0', '0', '0', '0', '0'], '3710': ['0.375628140703518', '1', '0', '0', '0', '0', '0'], '3715': ['0.373266078184111', '1', '0', '0', '0', '0', '0'], '3720': ['0.369289340101523', '1', '0', '0', '0', '0', '0'], '3725': ['0.363636363636364', '1', '0', '0', '0', '0', '0'], '3730': ['0.359536082474227', '1', '0', '0', '0', '0', '0'], '3735': ['0.35370611183355', '1', '0', '0', '0', '0', '0'], '3740': ['0.350326797385621', '1', '0', '0', '0', '0', '0'], '3745': ['0.346052631578947', '1', '0', '0', '0', '0', '0'], '3750': ['0.339095744680851', '1', '0', '0', '0', '0', '0'], '3755': ['0.336448598130841', '1', '0', '0', '0', '0', '0'], '3760': ['0.331989247311828', '1', '0', '0', '0', '0', '0'], '3765': ['0.322888283378747', '1', '0', '0', '0', '0', '0'], '3770': ['0.315426997245179', '1', '0', '0', '0', '0', '0'], '3775': ['0.307799442896936', '1', '0', '0', '0', '0', '0'], '3780': ['0.30098452883263', '1', '0', '0', '0', '0', '0'], '3785': ['0.295035460992908', '1', '0', '0', '0', '0', '0'], '3790': ['0.287965616045845', '1', '0', '0', '0', '0', '0'], '3795': ['0.280752532561505', '1', '0', '0', '0', '0', '0'], '3800': ['0.275510204081633', '1', '0', '0', '0', '0', '0'], '3805': ['0.269117647058823', '1', '0', '0', '0', '0', '0'], '3810': ['0.265878877400295', '1', '0', '0', '0', '0', '0'], '3815': ['0.262611275964392', '1', '0', '0', '0', '0', '0'], '3820': ['0.255988023952096', '1', '0', '0', '0', '0', '0'], '3825': ['0.250377073906486', '1', '0', '0', '0', '0', '0'], '3830': ['0.241221374045801', '1', '0', '0', '0', '0', '0'], '3835': ['0.237730061349693', '1', '0', '0', '0', '0', '0'], '3840': ['0.231839258114374', '1', '0', '0', '0', '0', '0'], '3845': ['0.225856697819315', '1', '0', '0', '0', '0', '0'], '3850': ['0.221003134796238', '1', '0', '0', '0', '0', '0'], '3855': ['0.211111111111111', '1', '0', '0', '0', '0', '0'], '3860': ['0.20096463022508', '1', '0', '0', '0', '0', '0'], '3865': ['0.194489465153971', '1', '0', '0', '0', '0', '0'], '3870': ['0.18657937806874', '1', '0', '0', '0', '0', '0'], '3875': ['0.17986798679868', '1', '0', '0', '0', '0', '0'], '3880': ['0.170283806343907', '1', '0', '0', '0', '0', '0'], '3885': ['0.159052453468697', '1', '0', '0', '0', '0', '0'], '3890': ['0.154761904761905', '1', '0', '0', '0', '0', '0'], '3895': ['0.141623488773748', '1', '0', '0', '0', '0', '0'], '3900': ['0.135652173913043', '1', '0', '0', '0', '0', '0']}
    tiedLookup={'0': ['0', '0', '0', '0', '0', '0'], '5': ['0.104940878378378', '0', '0', '0', '0', '0'], '10': ['0.104395604395604', '0.25', '0', '0', '0', '0'], '15': ['0.104670912951168', '0.076923076923077', '0', '0', '0', '0'], '20': ['0.104936952340244', '0.035087719298246', '0', '0', '0', '0'], '25': ['0.104641168886979', '0.024390243902439', '0', '0', '0', '0'], '30': ['0.104522830556157', '0.017543859649123', '0', '0', '0', '0'], '35': ['0.104828186167899', '0.021897810218978', '0', '0', '0', '0'], '40': ['0.10498687664042', '0.018518518518519', '0', '0', '0', '0'], '45': ['0.105494505494506', '0.016393442622951', '0', '0', '0', '0'], '50': ['0.105903161618395', '0.019047619047619', '0', '0', '0', '0'], '55': ['0.106013363028953', '0.012345679012346', '0', '0', '0', '0'], '60': ['0.105663756436087', '0.026415094339623', '0', '0', '0', '0'], '65': ['0.105914099392849', '0.021201413427562', '0', '0', '0', '0'], '70': ['0.10627690913211', '0.018987341772152', '0', '0', '0', '0'], '75': ['0.106285714285714', '0.01699716713881', '0', '0', '0', '0'], '80': ['0.106231317544263', '0.007936507936508', '0', '0', '0', '0'], '85': ['0.106648199445983', '0.007594936708861', '0', '0', '0', '0'], '90': ['0.106363214119833', '0.011933174224344', '0', '0', '0', '0'], '95': ['0.106750759168419', '0.006802721088435', '0.071428571428572', '0', '0', '0'], '100': ['0.106798400376382', '0.012738853503185', '0.071428571428572', '0', '0', '0'], '105': ['0.107007575757576', '0.008080808080808', '0.0625', '0', '0', '0'], '110': ['0.107534573199809', '0.007648183556405', '0.111111111111111', '0', '0', '0'], '115': ['0.107245681381958', '0.010928961748634', '0.111111111111111', '0', '0', '0'], '120': ['0.107944940835547', '0.010471204188482', '0.095238095238095', '0', '0', '0'], '125': ['0.108193532701191', '0.010016694490818', '0.086956521739131', '0', '0', '0'], '130': ['0.108015640273705', '0.014563106796117', '0.08', '0', '0', '0'], '135': ['0.107948969578018', '0.017405063291139', '0.074074074074074', '0', '0', '0'], '140': ['0.108148148148148', '0.019847328244275', '0.066666666666667', '0', '0', '0'], '145': ['0.107933349912957', '0.022026431718062', '0.060606060606061', '0', '0', '0'], '150': ['0.108141858141858', '0.020086083213773', '0.058823529411765', '0', '0', '0'], '155': ['0.108324974924774', '0.021156558533145', '0.052631578947369', '0', '0', '0'], '160': ['0.108564231738035', '0.022068965517241', '0.05', '0', '0', '0'], '165': ['0.108695652173913', '0.020352781546811', '0.047619047619048', '0', '0', '0'], '170': ['0.108739837398374', '0.022546419098143', '0.045454545454546', '0', '0', '0'], '175': ['0.109323116219668', '0.020779220779221', '0.061224489795918', '0', '0', '0'], '180': ['0.109799897383273', '0.024234693877551', '0.038461538461539', '0', '0', '0'], '185': ['0.110423116615067', '0.023661270236613', '0.036363636363636', '0', '0', '0'], '190': ['0.110966735966736', '0.024154589371981', '0.03448275862069', '0', '0', '0'], '195': ['0.111024033437827', '0.022511848341232', '0.048387096774194', '0', '0', '0'], '200': ['0.110527697558414', '0.024447031431898', '0.045454545454546', '0', '0', '0'], '205': ['0.110847189231987', '0.025085518814139', '0.044117647058824', '0', '0', '0'], '210': ['0.11063829787234', '0.023255813953488', '0.056338028169014', '0', '0', '0'], '215': ['0.111528150134048', '0.022532188841202', '0.055555555555556', '0', '0', '0'], '220': ['0.1112907572083', '0.021097046413502', '0.054054054054054', '0', '0', '0'], '225': ['0.111351937144405', '0.022774327122153', '0.052631578947369', '0', '0', '0'], '230': ['0.111806311207835', '0.022564102564103', '0.048780487804878', '0', '0', '0'], '235': ['0.112024102985483', '0.020060180541625', '0.047058823529412', '0', '0', '0'], '240': ['0.112889870273254', '0.019569471624266', '0.045454545454546', '0', '0', '0'], '245': ['0.113207547169811', '0.022157996146436', '0.044444444444445', '0', '0', '0'], '250': ['0.112632755729458', '0.024574669187146', '0.041237113402062', '0', '0', '0'], '255': ['0.112391121101433', '0.025139664804469', '0.04', '0', '0', '0'], '260': ['0.112270803949224', '0.024884792626728', '0.029411764705882', '0.25', '0', '0'], '265': ['0.112720045428734', '0.022583559168925', '0.038834951456311', '0.25', '0', '0'], '270': ['0.11314809510169', '0.021108179419525', '0.048076923076923', '0.25', '0', '0'], '275': ['0.113098672821696', '0.020761245674741', '0.054545454545455', '0.25', '0', '0'], '280': ['0.113788098693759', '0.019591141396934', '0.061946902654867', '0.25', '0', '0'], '285': ['0.113768961493582', '0.018487394957983', '0.070796460176991', '0.2', '0', '0'], '290': ['0.114369501466276', '0.01827242524917', '0.068965517241379', '0.166666666666667', '0', '0'], '295': ['0.114850900501919', '0.017142857142857', '0.068376068376068', '0.142857142857143', '0', '0'], '300': ['0.115041617122473', '0.018548387096774', '0.064', '0.142857142857143', '0', '0'], '305': ['0.115764283577625', '0.018253968253968', '0.063492063492064', '0.142857142857143', '0', '0'], '310': ['0.116033755274262', '0.01796875', '0.061068702290076', '0.142857142857143', '0', '0'], '315': ['0.116257947320618', '0.016266460108443', '0.066666666666667', '0.142857142857143', '0', '0'], '320': ['0.116087751371115', '0.019113149847095', '0.057553956834532', '0.142857142857143', '0', '0'], '325': ['0.115844315047502', '0.021148036253777', '0.056338028169014', '0.142857142857143', '0', '0'], '330': ['0.11565672100892', '0.021036814425244', '0.054794520547945', '0.125', '0', '0'], '335': ['0.114896252709817', '0.023014105419451', '0.052980132450331', '0.111111111111111', '0', '0'], '340': ['0.116054760423149', '0.023529411764706', '0.045751633986928', '0.111111111111111', '0', '0'], '345': ['0.115960099750623', '0.022710622710623', '0.045751633986928', '0.1', '0', '0'], '350': ['0.115119196988708', '0.021770682148041', '0.044025157232704', '0.090909090909091', '0', '0'], '355': ['0.115251026207768', '0.022922636103152', '0.043478260869565', '0.083333333333333', '0', '0'], '360': ['0.115873015873016', '0.021306818181818', '0.042424242424243', '0.076923076923077', '0', '0'], '365': ['0.116687979539642', '0.020365168539326', '0.046783625730994', '0.076923076923077', '0', '0'], '370': ['0.116458132820019', '0.020251396648045', '0.045977011494253', '0.076923076923077', '0', '0'], '375': ['0.116279069767442', '0.021453287197232', '0.04945054945055', '0.076923076923077', '0', '0'], '380': ['0.116482803374432', '0.020646937370957', '0.048128342245989', '0.071428571428572', '0', '0'], '385': ['0.116150081566069', '0.021174863387978', '0.046875', '0.066666666666667', '0', '0'], '390': ['0.116699539776463', '0.021577882670263', '0.045918367346939', '0.066666666666667', '0', '0'], '395': ['0.1166392092257', '0.022222222222222', '0.044776119402985', '0.066666666666667', '0', '0'], '400': ['0.116827082641885', '0.022044088176353', '0.042654028436019', '0.066666666666667', '0', '0'], '405': ['0.116201859229748', '0.020749665327979', '0.042056074766355', '0.0625', '0', '0'], '410': ['0.11623246492986', '0.020557029177719', '0.041666666666667', '0.055555555555556', '0', '0'], '415': ['0.116582914572864', '0.019179894179894', '0.041284403669725', '0.047619047619048', '0', '0'], '420': ['0.116874368474234', '0.019685039370079', '0.040723981900453', '0.045454545454546', '0', '0'], '425': ['0.117147707979626', '0.020077720207254', '0.04424778761062', '0.05', '0', '0'], '430': ['0.117486338797814', '0.019267822736031', '0.043859649122807', '0.045454545454546', '0', '0'], '435': ['0.117222413200413', '0.019047619047619', '0.039301310043668', '0.045454545454546', '0', '0'], '440': ['0.117932708983698', '0.018147684605757', '0.038961038961039', '0.043478260869565', '0', '0'], '445': ['0.117010129235068', '0.017945544554456', '0.043103448275862', '0.041666666666667', '0', '0'], '450': ['0.117626404494382', '0.019018404907976', '0.042918454935622', '0.041666666666667', '0', '0'], '455': ['0.116754850088183', '0.016413373860182', '0.051948051948052', '0.041666666666667', '0', '0'], '460': ['0.117647058823529', '0.017480409885473', '0.047826086956522', '0.041666666666667', '0', '0'], '465': ['0.118256520185781', '0.016666666666667', '0.047413793103448', '0.041666666666667', '0', '0'], '470': ['0.118637992831541', '0.018408551068884', '0.042194092827004', '0.041666666666667', '0', '0'], '475': ['0.119553474972992', '0.017730496453901', '0.04149377593361', '0.04', '0', '0'], '480': ['0.119942196531792', '0.016519174041298', '0.040650406504065', '0.038461538461539', '0', '0'], '485': ['0.120043652237177', '0.017595307917889', '0.039525691699605', '0.037037037037037', '0', '0'], '490': ['0.120746432491767', '0.017492711370262', '0.038910505836576', '0.03448275862069', '0', '0'], '495': ['0.120632585509378', '0.018539976825029', '0.038461538461539', '0.03448275862069', '0', '0'], '500': ['0.122032640949555', '0.019461934745278', '0.034749034749035', '0.03125', '0', '0'], '505': ['0.122859270290395', '0.019406392694064', '0.037878787878788', '0.03125', '0', '0'], '510': ['0.1226626776365', '0.019886363636364', '0.033962264150943', '0.028571428571429', '0', '0'], '515': ['0.122280570142536', '0.020963172804533', '0.041044776119403', '0.028571428571429', '0', '0'], '520': ['0.122356495468278', '0.020774845592364', '0.040740740740741', '0.028571428571429', '0', '0'], '525': ['0.122813688212928', '0.022271714922049', '0.04029304029304', '0.029411764705882', '0', '0'], '530': ['0.122285714285714', '0.021751254880089', '0.043010752688172', '0.028571428571429', '0', '0'], '535': ['0.122887864823349', '0.022099447513812', '0.042857142857143', '0.026315789473684', '0', '0'], '540': ['0.122685185185185', '0.02317880794702', '0.041522491349481', '0.026315789473684', '0', '0'], '545': ['0.123351435221102', '0.023026315789474', '0.041379310344828', '0.025641025641026', '0', '0'], '550': ['0.123490455784963', '0.023471615720524', '0.044982698961938', '0', '0', '0'], '555': ['0.123239436619718', '0.023939064200218', '0.047457627118644', '0', '0', '0'], '560': ['0.12347620920173', '0.023848238482385', '0.049833887043189', '0', '0', '0'], '565': ['0.12386228729719', '0.023243243243243', '0.05448717948718', '0', '0', '0'], '570': ['0.123805732484076', '0.023118279569893', '0.053627760252366', '0', '0', '0'], '575': ['0.123744475693049', '0.024468085106383', '0.053125', '0', '0', '0'], '580': ['0.123736352608168', '0.02431289640592', '0.052795031055901', '0', '0', '0'], '585': ['0.123376623376623', '0.024815205913411', '0.055045871559633', '0', '0', '0'], '590': ['0.123114553607827', '0.023771790808241', '0.053254437869823', '0', '0', '0'], '595': ['0.123102174805088', '0.024185068349106', '0.049707602339181', '0', '0', '0'], '600': ['0.121199671322925', '0.023696682464455', '0.048850574712644', '0', '0', '0'], '605': ['0.121413721413721', '0.024453694068679', '0.050991501416431', '0', '0', '0'], '610': ['0.122032486463973', '0.023970818134445', '0.050139275766017', '0', '0', '0'], '615': ['0.122338204592902', '0.02402088772846', '0.048780487804878', '0', '0', '0'], '620': ['0.123322147651007', '0.022384174908902', '0.048128342245989', '0', '0', '0'], '625': ['0.122895622895623', '0.021875', '0.049608355091384', '0', '0', '0'], '630': ['0.123096446700508', '0.024402907580478', '0.049095607235142', '0', '0', '0'], '635': ['0.124308216262239', '0.024289405684755', '0.046035805626599', '0', '0', '0'], '640': ['0.124946695095949', '0.02485758674262', '0.045112781954887', '0', '0', '0'], '645': ['0.125', '0.025270758122744', '0.04679802955665', '0', '0', '0'], '650': ['0.124839124839125', '0.02538860103627', '0.046341463414634', '0', '0', '0'], '655': ['0.124732104586369', '0.025520833333333', '0.045454545454546', '0', '0', '0'], '660': ['0.124515295131409', '0.027532467532468', '0.044811320754717', '0', '0', '0'], '665': ['0.125108225108225', '0.027489626556017', '0.044392523364486', '0', '0', '0'], '670': ['0.125977410947003', '0.026970954356847', '0.043778801843318', '0', '0', '0'], '675': ['0.126907980811164', '0.026383859286084', '0.043577981651376', '0', '0', '0'], '680': ['0.127631578947368', '0.026315789473684', '0.042792792792793', '0', '0', '0'], '685': ['0.128691053327457', '0.026694045174538', '0.040909090909091', '0.015384615384615', '0', '0'], '690': ['0.127716186252772', '0.027565084226646', '0.040816326530612', '0.014925373134328', '0', '0'], '695': ['0.128125', '0.027961362480936', '0.040178571428572', '0.014925373134328', '0', '0'], '700': ['0.127402771569066', '0.029501525940997', '0.037527593818985', '0.015151515151515', '0', '0'], '705': ['0.12657091561939', '0.029964448958862', '0.037199124726477', '0.014705882352941', '0', '0'], '710': ['0.127141568981064', '0.02979797979798', '0.037610619469027', '0.014084507042254', '0', '0'], '715': ['0.126976954360596', '0.028802425467408', '0.039387308533917', '0.013888888888889', '0', '0'], '720': ['0.127428829643019', '0.027918781725888', '0.040772532188841', '0.013888888888889', '0', '0'], '725': ['0.127157129881926', '0.02887537993921', '0.040339702760085', '0.013513513513514', '0', '0'], '730': ['0.126824817518248', '0.029813036887317', '0.040084388185654', '0.013157894736842', '0', '0'], '735': ['0.127347686669721', '0.030808080808081', '0.03950103950104', '0.013157894736842', '0', '0'], '740': ['0.127816091954023', '0.030792529025745', '0.039175257731959', '0.012658227848101', '0', '0'], '745': ['0.128406466512702', '0.030776992936428', '0.038539553752536', '0.0125', '0', '0'], '750': ['0.128703703703704', '0.030776992936428', '0.038229376257545', '0.0125', '0', '0'], '755': ['0.129767441860465', '0.030181086519115', '0.038', '0.012345679012346', '0', '0'], '760': ['0.129845866417562', '0.029633350075339', '0.037773359840954', '0.011904761904762', '0', '0'], '765': ['0.129455909943715', '0.028600100351229', '0.037475345167653', '0.011627906976744', '0', '0'], '770': ['0.13012729844413', '0.028514257128564', '0.037181996086106', '0.011494252873563', '0', '0'], '775': ['0.130393551446183', '0.027972027972028', '0.036608863198459', '0.011363636363636', '0', '0'], '780': ['0.130455407969639', '0.028028028028028', '0.036538461538462', '0.010989010989011', '0', '0'], '785': ['0.13', '0.027972027972028', '0.03639846743295', '0.010752688172043', '0', '0'], '790': ['0.127690100430416', '0.02788844621514', '0.036328871892926', '0.010526315789474', '0', '0'], '795': ['0.12763915547025', '0.030318091451292', '0.036121673003802', '0.010526315789474', '0', '0'], '800': ['0.126564003849856', '0.029835902536052', '0.033962264150943', '0.020408163265306', '0', '0'], '805': ['0.126147897535041', '0.028769841269841', '0.033834586466166', '0.02', '0', '0'], '810': ['0.126392251815981', '0.029791459781529', '0.033644859813084', '0.02', '0', '0'], '815': ['0.12688381137579', '0.030708271421496', '0.033582089552239', '0.01980198019802', '0', '0'], '820': ['0.12688381137579', '0.030738720872583', '0.03177570093458', '0.028846153846154', '0', '0'], '825': ['0.125911521633447', '0.027805362462761', '0.031598513011153', '0.019417475728155', '0.043478260869565', '0'], '830': ['0.125853658536585', '0.026772434308379', '0.033333333333333', '0.019047619047619', '0.043478260869565', '0'], '835': ['0.1262278978389', '0.028148148148148', '0.03302752293578', '0.018867924528302', '0.043478260869565', '0'], '840': ['0.126108374384236', '0.027695351137488', '0.032727272727273', '0.018348623853211', '0.041666666666667', '0'], '845': ['0.126175160811479', '0.029135802469136', '0.032608695652174', '0.017857142857143', '0.04', '0'], '850': ['0.12605459057072', '0.030123456790124', '0.030520646319569', '0.026548672566372', '0', '0'], '855': ['0.126058794220229', '0.030138339920949', '0.031914893617021', '0.026086956521739', '0', '0'], '860': ['0.126626626626627', '0.030183077684315', '0.034843205574913', '0.025641025641026', '0', '0'], '865': ['0.125377643504532', '0.030064070970922', '0.034722222222222', '0.025210084033614', '0', '0'], '870': ['0.124305204648813', '0.030571992110454', '0.034423407917384', '0.033333333333333', '0.038461538461539', '0'], '875': ['0.124873096446701', '0.031003937007874', '0.035958904109589', '0.03305785123967', '0.037037037037037', '0'], '880': ['0.126395939086294', '0.030049261083744', '0.037606837606838', '0.03305785123967', '0.035714285714286', '0'], '885': ['0.125319693094629', '0.029990167158309', '0.040336134453782', '0.03305785123967', '0.03448275862069', '0'], '890': ['0.125702606029637', '0.030556924593396', '0.040201005025126', '0.032786885245902', '0.03448275862069', '0'], '895': ['0.125641025641026', '0.030973451327434', '0.040201005025126', '0.032520325203252', '0.033333333333333', '0'], '900': ['0.126796714579055', '0.03189401373896', '0.040472175379427', '0.032', '0.033333333333333', '0'], '905': ['0.126484254001033', '0.032273838630807', '0.038590604026846', '0.031746031746032', '0.033333333333333', '0'], '910': ['0.127131782945736', '0.031831537708129', '0.038397328881469', '0.031007751937985', '0.035714285714286', '0'], '915': ['0.1282316442606', '0.031403336604514', '0.039735099337748', '0.031496062992126', '0.033333333333333', '0'], '920': ['0.12888198757764', '0.032003938946332', '0.03921568627451', '0.03125', '0.033333333333333', '0'], '925': ['0.129890453834116', '0.031847133757962', '0.038961038961039', '0.031007751937985', '0.033333333333333', '0'], '930': ['0.129251700680272', '0.032368808239333', '0.040064102564103', '0.031007751937985', '0.03448275862069', '0'], '935': ['0.130298273155416', '0.032940019665683', '0.038216560509554', '0.030769230769231', '0.03448275862069', '0'], '940': ['0.131371518654756', '0.031972454500738', '0.039308176100629', '0.030769230769231', '0.033333333333333', '0'], '945': ['0.130732735898788', '0.03295622233153', '0.038940809968847', '0.030769230769231', '0.033333333333333', '0'], '950': ['0.131259884027412', '0.032988675529296', '0.040688575899844', '0.02962962962963', '0.033333333333333', '0'], '955': ['0.131606765327696', '0.031972454500738', '0.043818466353678', '0.029197080291971', '0.032258064516129', '0'], '960': ['0.132235793945831', '0.032432432432433', '0.041731066460587', '0.029411764705882', '0.032258064516129', '0'], '965': ['0.131844763423711', '0.032448377581121', '0.040247678018576', '0.021428571428572', '0', '0'], '970': ['0.131663113006397', '0.031988188976378', '0.040061633281972', '0.020833333333333', '0', '0'], '975': ['0.131130063965885', '0.033464566929134', '0.0370942812983', '0.020689655172414', '0', '0'], '980': ['0.131762185324049', '0.033366045142296', '0.0370942812983', '0.02027027027027', '0', '0'], '985': ['0.131041890440387', '0.034398034398034', '0.036641221374046', '0.02027027027027', '0', '0'], '990': ['0.132004310344828', '0.034414945919371', '0.037993920972644', '0.02013422818792', '0', '0'], '995': ['0.132432432432432', '0.034906588003933', '0.036363636363636', '0.02', '0', '0'], '1000': ['0.132863340563991', '0.03494094488189', '0.035928143712575', '0.02013422818792', '0', '0'], '1005': ['0.133333333333333', '0.035311427170182', '0.037037037037037', '0.013422818791946', '0', '0'], '1010': ['0.133552271483306', '0.034889434889435', '0.038179148311307', '0.013333333333333', '0', '0'], '1015': ['0.133918770581778', '0.035942885278188', '0.037845705967977', '0.013071895424837', '0', '0'], '1020': ['0.134065934065934', '0.037000493339911', '0.03768115942029', '0.012820512820513', '0', '0'], '1025': ['0.134911894273128', '0.038118811881188', '0.035714285714286', '0.012738853503185', '0', '0'], '1030': ['0.133884297520661', '0.038728897715988', '0.03271692745377', '0.01875', '0', '0'], '1035': ['0.132782369146006', '0.037754595131644', '0.030042918454936', '0.030487804878049', '0', '0'], '1040': ['0.133592017738359', '0.037623762376238', '0.030085959885387', '0.029761904761905', '0', '0'], '1045': ['0.13270405330372', '0.039584364176151', '0.027181688125894', '0.029761904761905', '0', '0'], '1050': ['0.132328308207705', '0.040493827160494', '0.027065527065527', '0.029239766081871', '0', '0'], '1055': ['0.132476243711571', '0.040513833992095', '0.027027027027027', '0.029069767441861', '0', '0'], '1060': ['0.133707865168539', '0.039050914483441', '0.026760563380282', '0.028735632183908', '0', '0'], '1065': ['0.133933595948227', '0.038099950519545', '0.026647966339411', '0.028409090909091', '0', '0'], '1070': ['0.134125636672326', '0.038954635108481', '0.025316455696203', '0.027624309392265', '0', '0'], '1075': ['0.13496583143508', '0.038480513073508', '0.026573426573427', '0.026455026455027', '0', '0'], '1080': ['0.135612535612536', '0.038005923000987', '0.026536312849162', '0.026315789473684', '0', '0'], '1085': ['0.135661133371494', '0.038404726735598', '0.026647966339411', '0.025510204081633', '0', '0'], '1090': ['0.134948096885813', '0.038197845249755', '0.028129395218003', '0.025125628140704', '0', '0'], '1095': ['0.134837962962963', '0.03761602344895', '0.02820874471086', '0.025125628140704', '0', '0'], '1100': ['0.135780885780886', '0.038442822384428', '0.02820874471086', '0.024630541871921', '0', '0'], '1105': ['0.13599062133646', '0.039339485186984', '0.029494382022472', '0.024271844660194', '0', '0'], '1110': ['0.136470588235294', '0.038797284190107', '0.030898876404494', '0.023923444976077', '0', '0'], '1115': ['0.136953955135773', '0.039301310043668', '0.032212885154062', '0.023474178403756', '0', '0'], '1120': ['0.136417556346382', '0.039301310043668', '0.034722222222222', '0.023255813953488', '0', '0'], '1125': ['0.136228435455086', '0.039767216294859', '0.034578146611342', '0.023255813953488', '0', '0'], '1130': ['0.137231503579952', '0.040232670867669', '0.034435261707989', '0.023255813953488', '0', '0'], '1135': ['0.137581893984515', '0.040796503156872', '0.034530386740332', '0.023041474654378', '0', '0'], '1140': ['0.136716417910448', '0.041767848470131', '0.03448275862069', '0.022831050228311', '0', '0'], '1145': ['0.137910447761194', '0.041767848470131', '0.034578146611342', '0.022831050228311', '0', '0'], '1150': ['0.137454981992797', '0.041707080504365', '0.03448275862069', '0.022421524663677', '0', '0'], '1155': ['0.138387484957882', '0.042253521126761', '0.032921810699589', '0.026666666666667', '0', '0'], '1160': ['0.140108238123873', '0.04390243902439', '0.032742155525239', '0.026315789473684', '0', '0'], '1165': ['0.139492753623188', '0.044725328147788', '0.032831737346101', '0.026200873362446', '0', '0'], '1170': ['0.137243047158404', '0.045321637426901', '0.034106412005457', '0.025641025641026', '0', '0'], '1175': ['0.137910085054678', '0.047735021919143', '0.030013642564802', '0.024896265560166', '0', '0'], '1180': ['0.13980463980464', '0.047711781888997', '0.029810298102981', '0.024691358024691', '0', '0'], '1185': ['0.140923076923077', '0.047849202513292', '0.031550068587106', '0.023809523809524', '0', '0'], '1190': ['0.140740740740741', '0.046927914852443', '0.03265306122449', '0.023809523809524', '0', '0'], '1195': ['0.138871667699938', '0.048355899419729', '0.031039136302294', '0.02390438247012', '0', '0'], '1200': ['0.138490330630069', '0.048309178743961', '0.030748663101604', '0.0199203187251', '0.019607843137255', '0'], '1205': ['0.138490330630069', '0.048309178743961', '0.030748663101604', '0.0199203187251', '0.019607843137255', '0'], '1210': ['0.138576779026217', '0.048355899419729', '0.030625832223702', '0.0199203187251', '0.02', '0'], '1215': ['0.137672090112641', '0.049323017408124', '0.030625832223702', '0.019685039370079', '0.02', '0'], '1220': ['0.137562814070352', '0.048815853069116', '0.029100529100529', '0.023622047244095', '0.02', '0'], '1225': ['0.137974683544304', '0.04954304954305', '0.026595744680851', '0.027027027027027', '0.019607843137255', '0'], '1230': ['0.137142857142857', '0.049614643545279', '0.026525198938992', '0.026515151515152', '0.019230769230769', '0'], '1235': ['0.136681500317864', '0.048721659430777', '0.02774108322325', '0.026515151515152', '0.018518518518519', '0'], '1240': ['0.136653895274585', '0.049085659287777', '0.027667984189723', '0.026615969581749', '0.018181818181818', '0'], '1245': ['0.136363636363636', '0.050626808100289', '0.027522935779817', '0.026515151515152', '0.017241379310345', '0'], '1250': ['0.13470173187941', '0.052123552123552', '0.027379400260756', '0.026615969581749', '0.016666666666667', '0'], '1255': ['0.138242894056848', '0.05019305019305', '0.027096774193548', '0.026515151515152', '0.016393442622951', '0'], '1260': ['0.137975499677627', '0.050412021328163', '0.026888604353393', '0.026717557251908', '0.015873015873016', '0'], '1265': ['0.139519792342635', '0.052173913043478', '0.025608194622279', '0.026415094339623', '0.015873015873016', '0'], '1270': ['0.139397905759162', '0.051516610495908', '0.026819923371648', '0.026022304832714', '0.015873015873016', '0'], '1275': ['0.139841688654354', '0.051923076923077', '0.026582278481013', '0.026022304832714', '0.015384615384615', '0'], '1280': ['0.138962765957447', '0.050888142102737', '0.027603513174404', '0.026119402985075', '0.014925373134328', '0'], '1285': ['0.138297872340426', '0.05083932853717', '0.029040404040404', '0.025830258302583', '0.014925373134328', '0'], '1290': ['0.139720558882236', '0.051649928263989', '0.029299363057325', '0.025641025641026', '0.014925373134328', '0'], '1295': ['0.138926174496644', '0.052806850618459', '0.029449423815621', '0.02536231884058', '0.014285714285714', '0'], '1300': ['0.138814016172507', '0.053257251545411', '0.029374201787995', '0.025179856115108', '0.014084507042254', '0'], '1305': ['0.138398914518318', '0.054554079696395', '0.027989821882952', '0.021660649819495', '0.027027027027027', '0'], '1310': ['0.140434192672999', '0.054657794676806', '0.026649746192893', '0.021505376344086', '0.027027027027027', '0'], '1315': ['0.140720598232495', '0.054787994282992', '0.026515151515152', '0.021276595744681', '0.026666666666667', '0'], '1320': ['0.141882673942701', '0.054441260744986', '0.02625', '0.021276595744681', '0.025974025974026', '0'], '1325': ['0.14275956284153', '0.055076628352491', '0.02605459057072', '0.021201413427562', '0.025641025641026', '0'], '1330': ['0.143445435827042', '0.053665548634404', '0.027093596059113', '0.020979020979021', '0.025974025974026', '0'], '1335': ['0.144137931034483', '0.053262955854127', '0.028083028083028', '0.020761245674741', '0.025974025974026', '0'], '1340': ['0.144727773949001', '0.052986512524085', '0.027912621359223', '0.020761245674741', '0.025641025641026', '0'], '1345': ['0.144536652835408', '0.052530120481928', '0.027777777777778', '0.020689655172414', '0.025316455696203', '0'], '1350': ['0.144050104384134', '0.051516610495908', '0.030048076923077', '0.020618556701031', '0.024691358024691', '0'], '1355': ['0.144957983193277', '0.052808449351896', '0.028846153846154', '0.020477815699659', '0.025', '0'], '1360': ['0.145352900069881', '0.052454282964389', '0.028846153846154', '0.020618556701031', '0.023809523809524', '0'], '1365': ['0.145251396648045', '0.052098408104197', '0.029904306220096', '0.020689655172414', '0.023529411764706', '0'], '1370': ['0.145059565522074', '0.051923076923077', '0.028811524609844', '0.020761245674741', '0.023529411764706', '0'], '1375': ['0.143864598025388', '0.052378664103796', '0.028673835125448', '0.020408163265306', '0.023809523809524', '0'], '1380': ['0.142958244869073', '0.055288461538462', '0.026097271648873', '0.020408163265306', '0.023809523809524', '0'], '1385': ['0.142755681818182', '0.055341674687199', '0.027186761229315', '0.02027027027027', '0.023255813953488', '0'], '1390': ['0.142348754448399', '0.055984555984556', '0.026900584795322', '0.020408163265306', '0.02247191011236', '0'], '1395': ['0.142045454545455', '0.056310679611651', '0.026900584795322', '0.01980198019802', '0.02247191011236', '0'], '1400': ['0.142045454545455', '0.056365403304179', '0.025821596244132', '0.022875816993464', '0.021978021978022', '0'], '1405': ['0.143571428571429', '0.056119980648283', '0.024793388429752', '0.022653721682848', '0.021739130434783', '0'], '1410': ['0.142857142857143', '0.057170542635659', '0.025912838633687', '0.022801302931596', '0.021052631578947', '0'], '1415': ['0.142959770114943', '0.058139534883721', '0.024504084014002', '0.022801302931596', '0.021052631578947', '0'], '1420': ['0.145546705286025', '0.057831325301205', '0.024532710280374', '0.022801302931596', '0.020833333333333', '0'], '1425': ['0.146181818181818', '0.057349397590362', '0.023337222870479', '0.022950819672131', '0.019417475728155', '0'], '1430': ['0.145560407569141', '0.057915057915058', '0.023282887077998', '0.022950819672131', '0.019047619047619', '0'], '1435': ['0.145243282498184', '0.058111380145279', '0.023228803716609', '0.022875816993464', '0.019047619047619', '0'], '1440': ['0.144717800289436', '0.059252064108791', '0.023201856148492', '0.022801302931596', '0.019230769230769', '0'], '1445': ['0.146676300578035', '0.06022340942205', '0.023364485981309', '0.025889967637541', '0.018867924528302', '0'], '1450': ['0.146376811594203', '0.060768108896451', '0.023255813953488', '0.025889967637541', '0.018691588785047', '0'], '1455': ['0.144508670520231', '0.061064973131412', '0.023121387283237', '0.026143790849673', '0.018018018018018', '0'], '1460': ['0.143790849673203', '0.061674008810573', '0.024027459954234', '0.022875816993464', '0.027027027027027', '0'], '1465': ['0.143379663496708', '0.0625', '0.023917995444191', '0.019736842105263', '0.035398230088496', '0'], '1470': ['0.142857142857143', '0.063600782778865', '0.022701475595914', '0.019543973941368', '0.035398230088496', '0'], '1475': ['0.141495601173021', '0.064247179990191', '0.023782559456399', '0.019417475728155', '0.035087719298246', '0'], '1480': ['0.142124542124542', '0.065356265356265', '0.022675736961451', '0.019230769230769', '0.035087719298246', '0'], '1485': ['0.140234948604993', '0.06480117820324', '0.022727272727273', '0.019417475728155', '0.033333333333333', '0'], '1490': ['0.140014738393515', '0.06440511307768', '0.022522522522523', '0.019543973941368', '0.032786885245902', '0'], '1495': ['0.138868479059515', '0.065185185185185', '0.02247191011236', '0.019543973941368', '0.032258064516129', '0'], '1500': ['0.137573964497041', '0.065024630541872', '0.0234375', '0.019607843137255', '0.03305785123967', '0'], '1505': ['0.137037037037037', '0.066009852216749', '0.022346368715084', '0.01948051948052', '0.03305785123967', '0'], '1510': ['0.139673105497771', '0.066074950690335', '0.0234375', '0.019230769230769', '0.032786885245902', '0'], '1515': ['0.139985107967238', '0.066831683168317', '0.022222222222222', '0.018987341772152', '0.032', '0'], '1520': ['0.140193885160328', '0.067130780706116', '0.022002200220022', '0.018867924528302', '0.032', '0'], '1525': ['0.138059701492537', '0.067164179104478', '0.023153252480706', '0.021604938271605', '0.024390243902439', '0'], '1530': ['0.138266068759342', '0.066600397614314', '0.024282560706402', '0.021671826625387', '0.024590163934426', '0'], '1535': ['0.138369483919222', '0.066567312468952', '0.024282560706402', '0.021671826625387', '0.024793388429752', '0'], '1540': ['0.138426626323752', '0.066303809995052', '0.024229074889868', '0.021406727828746', '0.024590163934426', '0'], '1545': ['0.138321995464853', '0.066004962779156', '0.025330396475771', '0.021148036253777', '0.024590163934426', '0'], '1550': ['0.140898705255141', '0.063829787234043', '0.027593818984548', '0.020833333333333', '0.024390243902439', '0'], '1555': ['0.142205323193916', '0.064051638530288', '0.027533039647577', '0.020648967551623', '0.024390243902439', '0'], '1560': ['0.142532221379833', '0.063278525161933', '0.027502750275028', '0.026392961876833', '0.016393442622951', '0'], '1565': ['0.142424242424242', '0.064307078763709', '0.027563395810364', '0.026392961876833', '0.016260162601626', '0'], '1570': ['0.141437308868502', '0.065671641791045', '0.027442371020856', '0.028985507246377', '0.008264462809917', '0'], '1575': ['0.141429669485012', '0.066766317887394', '0.026030368763558', '0.029411764705882', '0.008130081300813', '0'], '1580': ['0.140540540540541', '0.067164179104478', '0.02835332606325', '0.025936599423631', '0.008064516129032', '0'], '1585': ['0.140418929402638', '0.067594433399602', '0.028260869565217', '0.026011560693642', '0.007874015748032', '0'], '1590': ['0.141414141414141', '0.066666666666667', '0.028230184581976', '0.028818443804035', '0.0078125', '0'], '1595': ['0.142523364485981', '0.067264573991031', '0.028199566160521', '0.028571428571429', '0.007751937984496', '0'], '1600': ['0.144080996884735', '0.067432567432568', '0.028169014084507', '0.028409090909091', '0.00763358778626', '0'], '1605': ['0.145849495733126', '0.064791562029131', '0.032327586206897', '0.025423728813559', '0.007692307692308', '0'], '1610': ['0.143740340030912', '0.064271255060729', '0.034445640473628', '0.024930747922438', '0.007575757575758', '0'], '1615': ['0.144615384615385', '0.065439672801636', '0.035106382978723', '0.024861878453039', '0.007407407407407', '0'], '1620': ['0.143410852713178', '0.066836734693878', '0.035031847133758', '0.024590163934426', '0.007407407407407', '0'], '1625': ['0.144297905352987', '0.065849923430322', '0.036208732694356', '0.024456521739131', '0.007299270072993', '0'], '1630': ['0.14519906323185', '0.065782763895972', '0.036055143160127', '0.024324324324324', '0.007299270072993', '0'], '1635': ['0.144644253322909', '0.066326530612245', '0.036016949152542', '0.024258760107817', '0.007246376811594', '0'], '1640': ['0.144321766561514', '0.067005076142132', '0.035106382978723', '0.026737967914439', '0.007194244604317', '0'], '1645': ['0.144549763033175', '0.068020304568528', '0.036170212765958', '0.023936170212766', '0.007194244604317', '0'], '1650': ['0.144215530903328', '0.068193384223919', '0.036958817317846', '0.024', '0.007042253521127', '0'], '1655': ['0.142517814726841', '0.068437180796731', '0.036803364879075', '0.023809523809524', '0.007142857142857', '0'], '1660': ['0.143764892772041', '0.069672131147541', '0.035306334371755', '0.024', '0.007194244604317', '0'], '1665': ['0.143312101910828', '0.069230769230769', '0.035051546391753', '0.024128686327078', '0.007246376811594', '0'], '1670': ['0.144915932746197', '0.068983137455289', '0.03416149068323', '0.023872679045093', '0.007246376811594', '0'], '1675': ['0.144354838709677', '0.068437180796731', '0.035087719298246', '0.023872679045093', '0.007042253521127', '0'], '1680': ['0.144238517324738', '0.068682726806766', '0.036960985626283', '0.023809523809524', '0.007042253521127', '0'], '1685': ['0.145631067961165', '0.068682726806766', '0.038026721479959', '0.023622047244095', '0.006896551724138', '0'], '1690': ['0.146440129449838', '0.068717948717949', '0.039094650205761', '0.023560209424084', '0.006849315068493', '0'], '1695': ['0.143780290791599', '0.07135523613963', '0.03913491246138', '0.023560209424084', '0.006802721088435', '0'], '1700': ['0.145748987854251', '0.072270630445925', '0.039256198347108', '0.023498694516971', '0.006756756756757', '0'], '1705': ['0.144822006472492', '0.071868583162218', '0.041450777202073', '0.023376623376623', '0.006666666666667', '0'], '1710': ['0.145292207792208', '0.070914696813977', '0.044513457556936', '0.020460358056266', '0.006711409395973', '0'], '1715': ['0.145646867371847', '0.070841889117043', '0.044513457556936', '0.020408163265306', '0.006711409395973', '0'], '1720': ['0.146481178396072', '0.071282051282051', '0.043433298862461', '0.02020202020202', '0.006756756756757', '0'], '1725': ['0.145662847790507', '0.069922879177378', '0.043254376930999', '0.020253164556962', '0.006666666666667', '0'], '1730': ['0.144026186579378', '0.071170706549768', '0.043254376930999', '0.02', '0.006622516556291', '0'], '1735': ['0.141455437448896', '0.070020746887967', '0.044806517311609', '0.020050125313283', '0.006622516556291', '0'], '1740': ['0.139344262295082', '0.071651090342679', '0.04369918699187', '0.022443890274314', '0.006711409395973', '0'], '1745': ['0.140148392415499', '0.072576464489373', '0.043478260869565', '0.022556390977444', '0.006666666666667', '0'], '1750': ['0.140278917145201', '0.074362974518981', '0.041624365482234', '0.022277227722772', '0.006849315068493', '0'], '1755': ['0.141205615194055', '0.07420861442657', '0.041624365482234', '0.022167487684729', '0.006802721088435', '0'], '1760': ['0.14297520661157', '0.073842953718149', '0.043522267206478', '0.019559902200489', '0.006849315068493', '0'], '1765': ['0.143920595533499', '0.073221757322176', '0.044176706827309', '0.019512195121951', '0.006756756756757', '0'], '1770': ['0.144159072079536', '0.072851153039832', '0.045', '0.019512195121951', '0.006666666666667', '0'], '1775': ['0.146058091286307', '0.072812991094814', '0.045362903225807', '0.019138755980861', '0.006666666666667', '0'], '1780': ['0.14654454621149', '0.07386066003143', '0.043303121852971', '0.019138755980861', '0.006578947368421', '0'], '1785': ['0.1475', '0.07318348144276', '0.044534412955466', '0.016627078384798', '0.006622516556291', '0'], '1790': ['0.149958574979287', '0.072889355007866', '0.043788187372709', '0.016509433962264', '0.006666666666667', '0'], '1795': ['0.149253731343284', '0.073568050446663', '0.043788187372709', '0.016393442622951', '0.006622516556291', '0'], '1800': ['0.148671096345515', '0.075709779179811', '0.042857142857143', '0.016241299303944', '0.006622516556291', '0'], '1805': ['0.150375939849624', '0.076115485564305', '0.042726347914547', '0.016241299303944', '0.006578947368421', '0'], '1810': ['0.151085141903172', '0.075749605470805', '0.042726347914547', '0.016166281755196', '0.006535947712418', '0'], '1815': ['0.151591289782245', '0.075382182393253', '0.041497975708502', '0.016091954022989', '0.006535947712418', '0'], '1820': ['0.149957877000842', '0.076963626779125', '0.041289023162135', '0.015945330296128', '0.006666666666667', '0'], '1825': ['0.148241206030151', '0.077453580901857', '0.042126379137412', '0.015873015873016', '0.006756756756757', '0'], '1830': ['0.147623019182652', '0.07684098185699', '0.044', '0.015765765765766', '0.006756756756757', '0'], '1835': ['0.150501672240803', '0.075401069518717', '0.043956043956044', '0.015555555555556', '0.006896551724138', '0'], '1840': ['0.149916247906198', '0.0768', '0.042253521126761', '0.015418502202643', '0.006849315068493', '0'], '1845': ['0.149152542372881', '0.077330508474576', '0.043346774193548', '0.015317286652079', '0.006802721088435', '0'], '1850': ['0.149532710280374', '0.077777777777778', '0.04251012145749', '0.015217391304348', '0.006802721088435', '0'], '1855': ['0.151023890784983', '0.077248677248677', '0.04263959390863', '0.015021459227468', '0.006711409395973', '0'], '1860': ['0.151411462788708', '0.076557550158395', '0.043877551020408', '0.014925373134328', '0.006666666666667', '0'], '1865': ['0.150343642611684', '0.076476793248945', '0.043877551020408', '0.014925373134328', '0.006666666666667', '0'], '1870': ['0.151332760103181', '0.078306878306878', '0.041624365482234', '0.014893617021277', '0.006711409395973', '0'], '1875': ['0.151411462788708', '0.078556263269639', '0.040650406504065', '0.014925373134328', '0.006622516556291', '0'], '1880': ['0.153977758768178', '0.078191489361702', '0.038383838383838', '0.01511879049676', '0.006578947368421', '0'], '1885': ['0.153977758768178', '0.078316462440064', '0.038383838383838', '0.015086206896552', '0.006535947712418', '0'], '1890': ['0.153780068728522', '0.077618288144604', '0.038461538461539', '0.015086206896552', '0.006493506493507', '0'], '1895': ['0.153846153846154', '0.076800847457627', '0.038500506585613', '0.015021459227468', '0.006535947712418', '0'], '1900': ['0.153846153846154', '0.077494692144374', '0.03951367781155', '0.015021459227468', '0.006369426751592', '0'], '1905': ['0.155765920826162', '0.077292110874201', '0.039634146341464', '0.014861995753716', '0.006289308176101', '0'], '1910': ['0.156946826758147', '0.078116639914393', '0.039593908629442', '0.016949152542373', '0.00625', '0'], '1915': ['0.156357388316151', '0.079271558650241', '0.037525354969574', '0.018987341772152', '0.006211180124224', '0'], '1920': ['0.156626506024096', '0.077873254564984', '0.039314516129032', '0.014767932489452', '0.0125', '0'], '1925': ['0.156896551724138', '0.078336034575905', '0.038961038961039', '0.014705882352941', '0.012422360248447', '0'], '1930': ['0.158031088082902', '0.078048780487805', '0.038805970149254', '0.014644351464435', '0.01219512195122', '0'], '1935': ['0.157712305025997', '0.079847908745247', '0.037623762376238', '0.016771488469602', '0.011904761904762', '0'], '1940': ['0.159090909090909', '0.078463203463204', '0.037586547972305', '0.016771488469602', '0.011834319526627', '0'], '1945': ['0.161545215100966', '0.077464788732394', '0.037254901960784', '0.016949152542373', '0.011627906976744', '0'], '1950': ['0.162114537444934', '0.075921908893709', '0.038160469667319', '0.016842105263158', '0.011627906976744', '0'], '1955': ['0.162687886825818', '0.077422847861397', '0.038048780487805', '0.014799154334038', '0.011695906432749', '0'], '1960': ['0.163120567375887', '0.076798269334776', '0.038272816486752', '0.016701461377871', '0.011764705882353', '0'], '1965': ['0.162210338680927', '0.076673866090713', '0.038235294117647', '0.01656314699793', '0.011904761904762', '0'], '1970': ['0.163992869875223', '0.075675675675676', '0.038310412573674', '0.016460905349794', '0.011976047904192', '0'], '1975': ['0.163247100802855', '0.077006507592191', '0.037109375', '0.016494845360825', '0.011976047904192', '0'], '1980': ['0.163247100802855', '0.076713819368879', '0.036929057337221', '0.01440329218107', '0.011976047904192', '0'], '1985': ['0.164125560538117', '0.078218359587181', '0.035992217898833', '0.014373716632444', '0.011834319526627', '0'], '1990': ['0.165022421524664', '0.077717391304348', '0.03609756097561', '0.014344262295082', '0.011695906432749', '0'], '1995': ['0.165919282511211', '0.077886710239652', '0.03515625', '0.014285714285714', '0.011494252873563', '0'], '2000': ['0.16711590296496', '0.077260273972603', '0.0357833655706', '0.014256619144603', '0.011428571428572', '0'], '2005': ['0.166967509025271', '0.079365079365079', '0.034816247582205', '0.01417004048583', '0.011494252873563', '0'], '2010': ['0.167724388032638', '0.08', '0.035748792270531', '0.014084507042254', '0.011299435028249', '0'], '2015': ['0.165013525698828', '0.081632653061225', '0.035645472061657', '0.014056224899598', '0.011173184357542', '0'], '2020': ['0.165461121157324', '0.082644628099174', '0.033653846153846', '0.014112903225807', '0.010989010989011', '0'], '2025': ['0.163023679417122', '0.084931506849315', '0.032913843175218', '0.013972055888224', '0.011049723756906', '0'], '2030': ['0.164684354986276', '0.084245076586433', '0.032038834951456', '0.015810276679842', '0.011111111111111', '0'], '2035': ['0.164673413063477', '0.084978070175439', '0.031884057971015', '0.015625', '0.01123595505618', '0'], '2040': ['0.16405529953917', '0.086291643910432', '0.030097087378641', '0.015748031496063', '0.010989010989011', '0'], '2045': ['0.164345403899721', '0.087241003271538', '0.030888030888031', '0.01577909270217', '0.011049723756906', '0'], '2050': ['0.163416898792943', '0.087431693989071', '0.031853281853282', '0.015686274509804', '0.010989010989011', '0'], '2055': ['0.164651162790698', '0.087123287671233', '0.030710172744722', '0.017751479289941', '0.010752688172043', '0'], '2060': ['0.164958061509786', '0.08781558726674', '0.031639501438159', '0.017716535433071', '0.010752688172043', '0'], '2065': ['0.166197183098592', '0.088122605363985', '0.032442748091603', '0.017821782178218', '0.010695187165775', '0'], '2070': ['0.167136150234742', '0.087719298245614', '0.032319391634981', '0.017892644135189', '0.010752688172043', '0'], '2075': ['0.169187145557656', '0.087266739846323', '0.034123222748815', '0.017716535433071', '0.010695187165775', '0'], '2080': ['0.169347209082308', '0.087458745874588', '0.03415559772296', '0.017543859649123', '0.010695187165775', '0'], '2085': ['0.169201520912548', '0.086717892425906', '0.035104364326376', '0.015625', '0.010582010582011', '0'], '2090': ['0.169829222011385', '0.086549062844543', '0.035104364326376', '0.015473887814313', '0.010638297872341', '0'], '2095': ['0.171591992373689', '0.087555066079295', '0.036156041864891', '0.015296367112811', '0.005405405405405', '0.014285714285714'], '2100': ['0.175572519083969', '0.086692435118719', '0.036087369420703', '0.015151515151515', '0.005464480874317', '0.014084507042254'], '2105': ['0.178399228543877', '0.086717892425906', '0.035204567078972', '0.01707779886148', '0.005405405405405', '0.013888888888889'], '2110': ['0.179190751445087', '0.086140254003313', '0.035950804162725', '0.016981132075472', '0.005405405405405', '0.013888888888889'], '2115': ['0.179090029041626', '0.085082872928177', '0.036931818181818', '0.016728624535316', '0.005494505494506', '0.013513513513514'], '2120': ['0.182608695652174', '0.082731815657968', '0.037593984962406', '0.016728624535316', '0.005524861878453', '0.013698630136986'], '2125': ['0.184719535783366', '0.082731815657968', '0.037700282752121', '0.016605166051661', '0.00561797752809', '0.013333333333333'], '2130': ['0.183317167798254', '0.083935519733185', '0.037593984962406', '0.016544117647059', '0.00561797752809', '0.013333333333333'], '2135': ['0.182974559686888', '0.083240843507214', '0.037523452157599', '0.01841620626151', '0.005464480874317', '0.013333333333333'], '2140': ['0.185365853658537', '0.083935519733185', '0.037700282752121', '0.01841620626151', '0.00531914893617', '0.013333333333333'], '2145': ['0.185185185185185', '0.084122562674095', '0.037664783427495', '0.018382352941177', '0.005291005291005', '0.013333333333333'], '2150': ['0.184031158714703', '0.083798882681564', '0.037629350893697', '0.018315018315018', '0.00531914893617', '0.013157894736842'], '2155': ['0.187743190661479', '0.085249579360628', '0.037523452157599', '0.018214936247723', '0.005347593582888', '0.012820512820513'], '2160': ['0.187683284457478', '0.085858585858586', '0.036482694106642', '0.019927536231884', '0.005434782608696', '0.012345679012346'], '2165': ['0.18958742632613', '0.085249579360628', '0.036414565826331', '0.019927536231884', '0.005434782608696', '0.012048192771084'], '2170': ['0.18836291913215', '0.086129753914989', '0.036380597014925', '0.020257826887661', '0.005263157894737', '0.011904761904762'], '2175': ['0.185074626865672', '0.087005019520357', '0.03544776119403', '0.020220588235294', '0.005208333333333', '0.011904761904762'], '2180': ['0.185332011892963', '0.08641975308642', '0.036111111111111', '0.02029520295203', '0.005181347150259', '0.012048192771084'], '2185': ['0.187314172447968', '0.085345311622684', '0.038033395176252', '0.020183486238532', '0.010309278350516', '0'], '2190': ['0.185515873015873', '0.084831460674157', '0.039069767441861', '0.02007299270073', '0.01025641025641', '0'], '2195': ['0.182452642073779', '0.083707865168539', '0.039106145251397', '0.019927536231884', '0.010204081632653', '0'], '2200': ['0.182089552238806', '0.083849184018008', '0.039069767441861', '0.01985559566787', '0.010416666666667', '0'], '2205': ['0.183266932270916', '0.083286437816545', '0.039179104477612', '0.01985559566787', '0.010309278350516', '0'], '2210': ['0.185', '0.083663086489542', '0.038104089219331', '0.019642857142857', '0.010204081632653', '0'], '2215': ['0.185370741482966', '0.084937712344281', '0.037998146431881', '0.019572953736655', '0.010204081632653', '0'], '2220': ['0.187', '0.085275724843661', '0.038924930491196', '0.017605633802817', '0.010309278350516', '0'], '2225': ['0.188188188188188', '0.084659090909091', '0.039888682745826', '0.016014234875445', '0.009950248756219', '0'], '2230': ['0.188068756319515', '0.084650112866817', '0.04096834264432', '0.015957446808511', '0.009950248756219', '0'], '2235': ['0.18762677484787', '0.085070422535211', '0.041938490214352', '0.014209591474245', '0.009852216748768', '0'], '2240': ['0.186925434116445', '0.086565486228218', '0.04089219330855', '0.014285714285714', '0.009756097560976', '0'], '2245': ['0.184156378600823', '0.088416340235031', '0.041044776119403', '0.014285714285714', '0.009615384615385', '0'], '2250': ['0.184156378600823', '0.087102177554439', '0.041275797373358', '0.01423487544484', '0.009615384615385', '0'], '2255': ['0.186022610483042', '0.086834733893558', '0.042452830188679', '0.013986013986014', '0.009615384615385', '0'], '2260': ['0.187435633367662', '0.086883408071749', '0.044090056285178', '0.012323943661972', '0.009661835748792', '0'], '2265': ['0.184917355371901', '0.086883408071749', '0.045028142589118', '0.012345679012346', '0.009569377990431', '0'], '2270': ['0.184074457083764', '0.08617795187465', '0.045325779036827', '0.012280701754386', '0.009569377990431', '0'], '2275': ['0.184074457083764', '0.086858432036097', '0.047752808988764', '0.010471204188482', '0.009433962264151', '0'], '2280': ['0.182286302780639', '0.088085827216262', '0.046948356807512', '0.010452961672474', '0.009433962264151', '0'], '2285': ['0.183026584867076', '0.089772727272727', '0.046554934823091', '0.010600706713781', '0.009345794392523', '0'], '2290': ['0.182281059063136', '0.090909090909091', '0.045412418906395', '0.010638297872341', '0.009174311926606', '0'], '2295': ['0.183026584867076', '0.090753424657534', '0.045581395348837', '0.010600706713781', '0.009009009009009', '0'], '2300': ['0.183673469387755', '0.091848450057405', '0.045412418906395', '0.01067615658363', '0.008658008658009', '0'], '2305': ['0.184156378600823', '0.092465753424658', '0.043761638733706', '0.012477718360071', '0.008547008547009', '0'], '2310': ['0.182751540041068', '0.094501718213059', '0.044651162790698', '0.010695187165775', '0.008438818565401', '0'], '2315': ['0.182751540041068', '0.095183486238532', '0.043802423112768', '0.010695187165775', '0.008264462809917', '0'], '2320': ['0.185375901132853', '0.094555873925502', '0.042910447761194', '0.010657193605684', '0.008264462809917', '0'], '2325': ['0.187822497420021', '0.094285714285714', '0.043233082706767', '0.010600706713781', '0.008196721311475', '0'], '2330': ['0.187628865979381', '0.093516924842226', '0.043030869971936', '0.010638297872341', '0.008230452674897', '0'], '2335': ['0.18595041322314', '0.094610091743119', '0.04311152764761', '0.010600706713781', '0.008264462809917', '0'], '2340': ['0.188541666666667', '0.095292766934558', '0.042830540037244', '0.010582010582011', '0.008264462809917', '0'], '2345': ['0.187695516162669', '0.096032202415181', '0.04182156133829', '0.012302284710018', '0.008333333333333', '0'], '2350': ['0.189727463312369', '0.095702005730659', '0.042671614100186', '0.012433392539965', '0.008298755186722', '0'], '2355': ['0.190376569037657', '0.097701149425287', '0.042513863216266', '0.0125', '0.008264462809917', '0'], '2360': ['0.189979123173278', '0.09919261822376', '0.040778498609824', '0.012302284710018', '0.00836820083682', '0'], '2365': ['0.191823899371069', '0.098729792147806', '0.040740740740741', '0.01219512195122', '0.008438818565401', '0'], '2370': ['0.191377497371188', '0.099654377880184', '0.041938490214352', '0.012068965517241', '0.008474576271186', '0'], '2375': ['0.192429022082019', '0.099307159353349', '0.041977611940299', '0.012006861063465', '0.008403361344538', '0'], '2380': ['0.193514644351464', '0.098550724637681', '0.041782729805014', '0.012048192771084', '0.008474576271186', '0'], '2385': ['0.19348054679285', '0.099652375434531', '0.042790697674419', '0.011945392491468', '0.008510638297872', '0'], '2390': ['0.195147679324895', '0.099015634047481', '0.04275092936803', '0.011986301369863', '0.008438818565401', '0'], '2395': ['0.194736842105263', '0.098550724637681', '0.043966323666979', '0.01188455008489', '0.008403361344538', '0'], '2400': ['0.196428571428571', '0.098312972658522', '0.042990654205608', '0.01188455008489', '0.00836820083682', '0'], '2405': ['0.196428571428571', '0.098312972658522', '0.042990654205608', '0.01188455008489', '0.00836820083682', '0'], '2410': ['0.196635120925342', '0.098255813953488', '0.043071161048689', '0.011844331641286', '0.00836820083682', '0'], '2415': ['0.195560253699789', '0.099303135888502', '0.042990654205608', '0.011824324324324', '0.00836820083682', '0'], '2420': ['0.19661733615222', '0.098665118978526', '0.042990654205608', '0.011844331641286', '0.008333333333333', '0'], '2425': ['0.195329087048832', '0.098786828422877', '0.044131455399061', '0.011824324324324', '0.008403361344538', '0'], '2430': ['0.194236926360726', '0.099537037037037', '0.044859813084112', '0.011804384485666', '0.008403361344538', '0'], '2435': ['0.195121951219512', '0.101685066821615', '0.04384328358209', '0.011824324324324', '0.008438818565401', '0'], '2440': ['0.198941798941799', '0.101339545719278', '0.043030869971936', '0.011744966442953', '0.008403361344538', '0'], '2445': ['0.20253164556962', '0.100467289719626', '0.042950513538749', '0.011764705882353', '0.00836820083682', '0'], '2450': ['0.203605514316013', '0.10122878876536', '0.041860465116279', '0.011725293132328', '0.008403361344538', '0'], '2455': ['0.204690831556503', '0.101694915254237', '0.041159962581852', '0.011570247933884', '0.008403361344538', '0'], '2460': ['0.204690831556503', '0.10122878876536', '0.042293233082707', '0.011475409836066', '0.008333333333333', '0'], '2465': ['0.207006369426752', '0.1015854374633', '0.041431261770245', '0.011456628477905', '0.008264462809917', '0'], '2470': ['0.207006369426752', '0.103001765744556', '0.041353383458647', '0.011456628477905', '0.008230452674897', '0'], '2475': ['0.207805907172996', '0.101944608131998', '0.039735099337748', '0.01141924959217', '0.008196721311475', '0'], '2480': ['0.208640674394099', '0.10408042578356', '0.039399624765479', '0.011532125205931', '0.008163265306122', '0'], '2485': ['0.208245243128964', '0.105263157894737', '0.03842549203374', '0.011494252873563', '0.008196721311475', '0'], '2490': ['0.209129511677282', '0.106445890005914', '0.038533834586466', '0.011400651465798', '0.008097165991903', '0'], '2495': ['0.209850107066381', '0.106658809664113', '0.03849765258216', '0.01141924959217', '0.008097165991903', '0'], '2500': ['0.20855614973262', '0.106257378984652', '0.039473684210526', '0.009771986970684', '0.008032128514056', '0'], '2505': ['0.209625668449198', '0.104919976289271', '0.041044776119403', '0.009868421052632', '0.007936507936508', '0'], '2510': ['0.210862619808307', '0.106420927467301', '0.039325842696629', '0.009852216748768', '0.007905138339921', '0'], '2515': ['0.212153518123667', '0.106078665077473', '0.039289055191768', '0.009852216748768', '0.0078125', '0'], '2520': ['0.215122470713525', '0.106993424985057', '0.039179104477612', '0.00990099009901', '0.007662835249042', '0'], '2525': ['0.218181818181818', '0.106801909307876', '0.03921568627451', '0.009884678747941', '0.00763358778626', '0'], '2530': ['0.218649517684887', '0.107334525939177', '0.040111940298508', '0.009884678747941', '0.007722007722008', '0'], '2535': ['0.220193340494092', '0.108076009501188', '0.039510818438382', '0.009836065573771', '0.007692307692308', '0'], '2540': ['0.218649517684887', '0.109328579916815', '0.038679245283019', '0.009819967266776', '0.007662835249042', '0'], '2545': ['0.21948608137045', '0.108799048751486', '0.038825757575758', '0.009819967266776', '0.00763358778626', '0'], '2550': ['0.222459893048128', '0.108059701492537', '0.039473684210526', '0.009884678747941', '0.007547169811321', '0'], '2555': ['0.223642172523962', '0.10984393757503', '0.039362699156514', '0.009884678747941', '0.007518796992481', '0'], '2560': ['0.222929936305732', '0.110240963855422', '0.039399624765479', '0.009819967266776', '0.007518796992481', '0'], '2565': ['0.224338624338624', '0.111312764670296', '0.038461538461539', '0.00978792822186', '0.007518796992481', '0'], '2570': ['0.229299363057325', '0.109903381642512', '0.03857008466604', '0.009771986970684', '0.007462686567164', '0'], '2575': ['0.231668437832093', '0.109167671893848', '0.037807183364839', '0.009756097560976', '0.007407407407407', '0'], '2580': ['0.236228813559322', '0.108761329305136', '0.037950664136622', '0.009677419354839', '0.007434944237918', '0'], '2585': ['0.234791889007471', '0.108839446782922', '0.038204393505253', '0.011182108626198', '0.00374531835206', '0'], '2590': ['0.23692636072572', '0.107035478051714', '0.039309683604986', '0.0128', '0', '0'], '2595': ['0.237539766702015', '0.106344410876133', '0.039423076923077', '0.0128', '0', '0'], '2600': ['0.236228813559322', '0.106925880923451', '0.040152963671128', '0.0128', '0', '0'], '2605': ['0.237037037037037', '0.106968215158924', '0.040152963671128', '0.012759170653908', '0', '0'], '2610': ['0.235729386892178', '0.10790925812385', '0.04', '0.012820512820513', '0', '0'], '2615': ['0.23784355179704', '0.107296137339056', '0.039010466222645', '0.0128', '0', '0'], '2620': ['0.237644584647739', '0.107493857493858', '0.040076335877863', '0.0128', '0', '0'], '2625': ['0.238947368421053', '0.107296137339056', '0.039234449760766', '0.012779552715655', '0', '0'], '2630': ['0.237894736842105', '0.10865561694291', '0.038240917782027', '0.012738853503185', '0', '0'], '2635': ['0.236649214659686', '0.109876543209877', '0.037072243346008', '0.012820512820513', '0', '0'], '2640': ['0.236458333333333', '0.109869646182495', '0.036931818181818', '0.012903225806452', '0', '0'], '2645': ['0.237696335078534', '0.1090458488228', '0.036018957345972', '0.012861736334405', '0', '0'], '2650': ['0.237341772151899', '0.110148514851485', '0.034905660377359', '0.014423076923077', '0', '0'], '2655': ['0.240506329113924', '0.107806691449814', '0.035950804162725', '0.014308426073132', '0', '0'], '2660': ['0.237894736842105', '0.110148514851485', '0.034188034188034', '0.014331210191083', '0', '0'], '2665': ['0.238600212089077', '0.110562075355158', '0.035037878787879', '0.012738853503185', '0', '0'], '2670': ['0.240466101694915', '0.11035758323058', '0.036190476190476', '0.011111111111111', '0', '0'], '2675': ['0.240425531914894', '0.112546125461255', '0.03530534351145', '0.011164274322169', '0', '0'], '2680': ['0.240976645435244', '0.112338858195212', '0.034515819750719', '0.011182108626198', '0', '0'], '2685': ['0.240466101694915', '0.112338858195212', '0.034648700673725', '0.011146496815287', '0', '0'], '2690': ['0.239199157007376', '0.112407862407862', '0.034816247582205', '0.011111111111111', '0', '0'], '2695': ['0.241850683491062', '0.111931119311193', '0.03484995159729', '0.011093502377179', '0', '0'], '2700': ['0.243953732912723', '0.111590628853268', '0.033816425120773', '0.011041009463722', '0', '0'], '2705': ['0.244747899159664', '0.111866501854141', '0.032818532818533', '0.011041009463722', '0', '0'], '2710': ['0.246056782334385', '0.110630407911001', '0.033718689788054', '0.011093502377179', '0', '0'], '2715': ['0.24630021141649', '0.11035758323058', '0.033783783783784', '0.012678288431062', '0', '0'], '2720': ['0.24789029535865', '0.109529702970297', '0.033621517771374', '0.012759170653908', '0', '0'], '2725': ['0.247357293868922', '0.109181141439206', '0.032598274209013', '0.014308426073132', '0', '0'], '2730': ['0.248414376321353', '0.110006215040398', '0.033492822966507', '0.012638230647709', '0', '0'], '2735': ['0.249208025343189', '0.111596009975062', '0.032380952380952', '0.012718600953895', '0', '0'], '2740': ['0.248945147679325', '0.113664596273292', '0.028873917228104', '0.012718600953895', '0', '0'], '2745': ['0.252136752136752', '0.11433868974042', '0.028708133971292', '0.0128', '0', '0'], '2750': ['0.254019292604502', '0.11495673671199', '0.028625954198473', '0.012861736334405', '0', '0'], '2755': ['0.254564983888292', '0.11557478368356', '0.027698185291309', '0.012841091492777', '0', '0'], '2760': ['0.251612903225806', '0.117501546072975', '0.027724665391969', '0.012759170653908', '0', '0'], '2765': ['0.251348435814455', '0.119209388511427', '0.027671755725191', '0.012820512820513', '0', '0'], '2770': ['0.249187432286024', '0.121454993834772', '0.02868068833652', '0.0128', '0', '0'], '2775': ['0.250270855904659', '0.120913016656385', '0.028763183125599', '0.0128', '0', '0'], '2780': ['0.253812636165577', '0.119384615384615', '0.028763183125599', '0.0128', '0', '0'], '2785': ['0.257297297297297', '0.117501546072975', '0.030622009569378', '0.011217948717949', '0', '0'], '2790': ['0.260021668472373', '0.115977791486737', '0.030710172744722', '0.011217948717949', '0', '0'], '2795': ['0.261723009814613', '0.115337423312883', '0.030858244937319', '0.0112', '0', '0'], '2800': ['0.262582056892779', '0.115196078431373', '0.030977734753146', '0.011164274322169', '0', '0'], '2805': ['0.263157894736842', '0.115196078431373', '0.031067961165049', '0.011111111111111', '0', '0'], '2810': ['0.266813671444322', '0.113831089351285', '0.031037827352085', '0.011111111111111', '0', '0'], '2815': ['0.263274336283186', '0.114373088685015', '0.032007759456838', '0.011128775834658', '0', '0'], '2820': ['0.264088397790055', '0.114110429447853', '0.031884057971015', '0.0112', '0', '0'], '2825': ['0.264026402640264', '0.115289765721332', '0.031791907514451', '0.011182108626198', '0', '0'], '2830': ['0.264026402640264', '0.113776137761378', '0.033980582524272', '0.0112', '0', '0'], '2835': ['0.265060240963855', '0.112415071031501', '0.034985422740525', '0.011164274322169', '0', '0'], '2840': ['0.26952695269527', '0.111247695144438', '0.035259549461313', '0.011111111111111', '0', '0'], '2845': ['0.267326732673267', '0.112684729064039', '0.034246575342466', '0.012658227848101', '0', '0'], '2850': ['0.269315673289183', '0.112068965517241', '0.0341796875', '0.012678288431062', '0', '0'], '2855': ['0.274033149171271', '0.109538461538462', '0.034414945919371', '0.012558869701727', '0', '0'], '2860': ['0.275633958103638', '0.110216718266254', '0.034414945919371', '0.012461059190031', '0', '0'], '2865': ['0.277839029768467', '0.109113453192808', '0.034313725490196', '0.012519561815337', '0', '0'], '2870': ['0.278327832783278', '0.108695652173913', '0.034313725490196', '0.012618296529969', '0', '0'], '2875': ['0.277412280701754', '0.108343711083437', '0.035433070866142', '0.012578616352201', '0', '0'], '2880': ['0.277533039647577', '0.109794135995009', '0.036168132942327', '0.01259842519685', '0', '0'], '2885': ['0.276127612761276', '0.11125', '0.035087719298246', '0.012638230647709', '0', '0'], '2890': ['0.274423710208562', '0.112507856693903', '0.0357833655706', '0.011111111111111', '0', '0'], '2895': ['0.274229074889868', '0.113350125944584', '0.035714285714286', '0.011075949367089', '0', '0'], '2900': ['0.27857935627081', '0.111879321181647', '0.035679845708775', '0.011058451816746', '0', '0'], '2905': ['0.279558011049724', '0.111041009463722', '0.035714285714286', '0.010989010989011', '0', '0'], '2910': ['0.282107574094402', '0.108296390120329', '0.037790697674419', '0.009389671361502', '0', '0'], '2915': ['0.284463894967177', '0.107369758576874', '0.036786060019361', '0.009419152276295', '0', '0'], '2920': ['0.283842794759825', '0.107142857142857', '0.037644787644788', '0.009375', '0', '0'], '2925': ['0.285087719298246', '0.107074569789675', '0.03757225433526', '0.009404388714734', '0', '0'], '2930': ['0.285400658616904', '0.108125399872041', '0.03639846743295', '0.009404388714734', '0', '0'], '2935': ['0.286343612334802', '0.108556832694764', '0.035508637236085', '0.009389671361502', '0', '0'], '2940': ['0.287280701754386', '0.106982703395259', '0.034715525554484', '0.009316770186335', '0', '0'], '2945': ['0.289473684210526', '0.107464607464607', '0.03444976076555', '0.009345794392523', '0', '0'], '2950': ['0.290889132821076', '0.1073264781491', '0.034615384615385', '0.007751937984496', '0', '0'], '2955': ['0.292307692307692', '0.106958762886598', '0.03444976076555', '0.00776397515528', '0', '0'], '2960': ['0.290710382513661', '0.107235142118863', '0.034715525554484', '0.007680491551459', '0', '0'], '2965': ['0.291028446389497', '0.107304460245637', '0.035679845708775', '0.006134969325153', '0', '0'], '2970': ['0.292257360959651', '0.107512953367876', '0.035679845708775', '0.006153846153846', '0', '0'], '2975': ['0.292709466811752', '0.106934543097861', '0.035818005808325', '0.006134969325153', '0', '0'], '2980': ['0.293028322440087', '0.10873786407767', '0.034985422740525', '0.00611620795107', '0', '0'], '2985': ['0.29379760609358', '0.107932379713914', '0.036857419980601', '0.004559270516717', '0', '0'], '2990': ['0.296655879180151', '0.105228758169935', '0.036821705426357', '0.004566210045662', '0', '0'], '2995': ['0.296655879180151', '0.105160026126715', '0.036929057337221', '0.004559270516717', '0', '0'], '3000': ['0.296739130434783', '0.1060507482108', '0.036929057337221', '0.004566210045662', '0', '0'], '3005': ['0.298701298701299', '0.10443864229765', '0.036893203883495', '0.004594180704441', '0', '0'], '3010': ['0.301948051948052', '0.105297580117724', '0.034816247582205', '0.004601226993865', '0', '0'], '3015': ['0.3', '0.105781865965834', '0.034985422740525', '0.004594180704441', '0', '0'], '3020': ['0.305103148751357', '0.105160026126715', '0.034985422740525', '0.004601226993865', '0', '0'], '3025': ['0.308615049073064', '0.105022831050228', '0.035887487875849', '0.003072196620584', '0', '0'], '3030': ['0.309368191721133', '0.105022831050228', '0.035121951219512', '0.003053435114504', '0', '0'], '3035': ['0.313253012048193', '0.104545454545455', '0.035363457760314', '0.003030303030303', '0', '0'], '3040': ['0.315098468271335', '0.104098893949252', '0.034313725490196', '0.003025718608169', '0', '0'], '3045': ['0.316831683168317', '0.104234527687296', '0.03411306042885', '0.003034901365706', '0', '0'], '3050': ['0.317127071823204', '0.104098893949252', '0.035019455252918', '0.003067484662577', '0', '0'], '3055': ['0.318281938325991', '0.103403141361257', '0.034749034749035', '0.003095975232198', '0', '0'], '3060': ['0.318632855567806', '0.103606557377049', '0.034615384615385', '0.003095975232198', '0', '0'], '3065': ['0.321507760532151', '0.102480417754569', '0.034682080924856', '0.003110419906687', '0', '0'], '3070': ['0.324053452115813', '0.102797657774886', '0.032786885245902', '0.003110419906687', '0', '0'], '3075': ['0.324053452115813', '0.102998696219035', '0.032818532818533', '0.003100775193798', '0', '0'], '3080': ['0.325503355704698', '0.102864583333333', '0.032660902977906', '0.003115264797508', '0', '0'], '3085': ['0.326256983240223', '0.10313315926893', '0.031700288184438', '0.003105590062112', '0', '0'], '3090': ['0.327354260089686', '0.104166666666667', '0.029980657640232', '0.003086419753086', '0', '0'], '3095': ['0.329583802024747', '0.103246753246753', '0.02992277992278', '0.003129890453834', '0', '0'], '3100': ['0.330337078651685', '0.103313840155945', '0.028985507246377', '0.003159557661927', '0', '0'], '3105': ['0.329571106094808', '0.104545454545455', '0.028901734104046', '0.003174603174603', '0', '0'], '3110': ['0.329171396140749', '0.105775470473718', '0.028901734104046', '0.003164556962025', '0', '0'], '3115': ['0.331050228310502', '0.105365223012282', '0.029126213592233', '0.003129890453834', '0', '0'], '3120': ['0.331058020477816', '0.106493506493506', '0.02909796314258', '0.003100775193798', '0', '0'], '3125': ['0.33144154370034', '0.107073329007138', '0.027237354085603', '0.003110419906687', '0', '0'], '3130': ['0.332957110609481', '0.106020942408377', '0.027131782945737', '0.003100775193798', '0', '0'], '3135': ['0.334836527621195', '0.105781865965834', '0.026112185686654', '0.003091190108192', '0', '0'], '3140': ['0.337485843714609', '0.10498687664042', '0.026137463697967', '0.003095975232198', '0', '0'], '3145': ['0.340909090909091', '0.103538663171691', '0.026112185686654', '0.003100775193798', '0', '0'], '3150': ['0.343215507411631', '0.102883355176933', '0.026036644165863', '0.003095975232198', '0', '0'], '3155': ['0.345183486238532', '0.1026814911707', '0.026011560693642', '0.003120124804992', '0', '0'], '3160': ['0.346375143843498', '0.103065883887802', '0.02512077294686', '0.003105590062112', '0', '0'], '3165': ['0.349369988545246', '0.101439790575916', '0.024108003857281', '0.003105590062112', '0', '0'], '3170': ['0.350114416475972', '0.100983606557377', '0.024061597690087', '0.003110419906687', '0', '0'], '3175': ['0.352673492605233', '0.099211563731932', '0.02323330106486', '0.003091190108192', '0', '0'], '3180': ['0.353075170842825', '0.099803020354563', '0.022330097087379', '0.003091190108192', '0', '0'], '3185': ['0.356979405034325', '0.098167539267016', '0.023346303501946', '0.001540832049307', '0', '0'], '3190': ['0.358533791523482', '0.097385620915033', '0.023506366307542', '0.001536098310292', '0', '0'], '3195': ['0.360730593607306', '0.096456692913386', '0.022526934378061', '0.001538461538462', '0', '0'], '3200': ['0.363532110091743', '0.095737704918033', '0.022439024390244', '0.001545595054096', '0', '0'], '3205': ['0.364678899082569', '0.095863427445831', '0.021400778210117', '0.001552795031056', '0', '0'], '3210': ['0.36697247706422', '0.095332018408942', '0.020447906523856', '0.001550387596899', '0', '0'], '3215': ['0.367816091954023', '0.095583388266315', '0.020348837209302', '0.001550387596899', '0', '0'], '3220': ['0.370799536500579', '0.095081967213115', '0.020368574199806', '0.001560062402496', '0', '0'], '3225': ['0.373255813953488', '0.093647675180092', '0.021317829457364', '0.0015625', '0', '0'], '3230': ['0.376744186046512', '0.092277486910995', '0.020329138431752', '0.001577287066246', '0', '0'], '3235': ['0.374418604651163', '0.093709043250328', '0.021256038647343', '0', '0', '0'], '3240': ['0.375145180023229', '0.093770491803279', '0.020348837209302', '0', '0', '0'], '3245': ['0.374275782155272', '0.094550229809586', '0.019361084220716', '0', '0', '0'], '3250': ['0.376306620209059', '0.094488188976378', '0.018375241779497', '0', '0', '0'], '3255': ['0.377030162412993', '0.095520421607378', '0.018286814244466', '0', '0', '0'], '3260': ['0.375870069605568', '0.096901779828609', '0.017307692307692', '0', '0', '0'], '3265': ['0.375145180023229', '0.097625329815304', '0.017391304347826', '0', '0', '0'], '3270': ['0.377777777777778', '0.097304404996713', '0.017391304347826', '0', '0', '0'], '3275': ['0.381796690307329', '0.096015676028739', '0.018393030009681', '0', '0', '0'], '3280': ['0.382248520710059', '0.096732026143791', '0.017458777885548', '0', '0', '0'], '3285': ['0.382422802850356', '0.097322011757022', '0.017374517374517', '0', '0', '0'], '3290': ['0.384982121573301', '0.097068403908795', '0.016441005802708', '0', '0', '0'], '3295': ['0.386634844868735', '0.096879063719116', '0.017391304347826', '0', '0', '0'], '3300': ['0.389221556886228', '0.095979247730221', '0.016441005802708', '0.001602564102564', '0', '0'], '3305': ['0.389891696750903', '0.096440129449838', '0.016536964980545', '0.001589825119237', '0', '0'], '3310': ['0.387290167865707', '0.098179453836151', '0.015458937198068', '0.001602564102564', '0', '0'], '3315': ['0.388221153846154', '0.099740932642487', '0.012645914396887', '0.001607717041801', '0', '0'], '3320': ['0.386826347305389', '0.099870298313878', '0.012670565302144', '0.001607717041801', '0', '0'], '3325': ['0.384982121573301', '0.100195185426155', '0.01364522417154', '0', '0', '0'], '3330': ['0.385167464114833', '0.101430429128739', '0.012658227848101', '0', '0', '0'], '3335': ['0.388489208633094', '0.101364522417154', '0.012682926829268', '0', '0', '0'], '3340': ['0.389952153110048', '0.10149642160052', '0.0126953125', '0', '0', '0'], '3345': ['0.392086330935252', '0.100518806744488', '0.012745098039216', '0', '0', '0'], '3350': ['0.392814371257485', '0.099805573558004', '0.012782694198623', '0', '0', '0'], '3355': ['0.392814371257485', '0.099805573558004', '0.012820512820513', '0', '0', '0'], '3360': ['0.398092967818832', '0.096479791395046', '0.012770137524558', '0', '0', '0'], '3365': ['0.401913875598086', '0.094928478543563', '0.012858555885262', '0', '0', '0'], '3370': ['0.40625', '0.094620868438108', '0.010934393638171', '0', '0', '0'], '3375': ['0.407673860911271', '0.09375', '0.010912698412699', '0', '0', '0'], '3380': ['0.409090909090909', '0.094056172436316', '0.008973080757727', '0', '0', '0'], '3385': ['0.407894736842105', '0.094647519582246', '0.008955223880597', '0', '0', '0'], '3390': ['0.410287081339713', '0.093933463796478', '0.007992007992008', '0', '0', '0'], '3395': ['0.410714285714286', '0.093647675180092', '0.007028112449799', '0', '0', '0'], '3400': ['0.414081145584726', '0.092217135382603', '0.007070707070707', '0', '0', '0'], '3405': ['0.416666666666667', '0.090373280943026', '0.00709939148073', '0', '0', '0'], '3410': ['0.417857142857143', '0.090196078431373', '0.006128702757916', '0', '0', '0'], '3415': ['0.41816009557945', '0.091205211726384', '0.005128205128205', '0', '0', '0'], '3420': ['0.421615201900238', '0.088466579292267', '0.00513874614594', '0', '0', '0'], '3425': ['0.425178147268409', '0.08655737704918', '0.005144032921811', '0', '0', '0'], '3430': ['0.425531914893617', '0.085582620144832', '0.00515995872033', '0', '0', '0'], '3435': ['0.429594272076372', '0.084856396866841', '0.005197505197505', '0', '0', '0'], '3440': ['0.437574316290131', '0.080655737704918', '0.00624349635796', '0', '0', '0'], '3445': ['0.438763376932224', '0.080708661417323', '0.005246589716684', '0', '0', '0'], '3450': ['0.442583732057416', '0.079738562091503', '0.005296610169492', '0', '0', '0'], '3455': ['0.444711538461538', '0.079582517938682', '0.005307855626327', '0', '0', '0'], '3460': ['0.445378151260504', '0.079033311561071', '0.00534188034188', '0', '0', '0'], '3465': ['0.446300715990453', '0.077580539119001', '0.00531914893617', '0', '0', '0'], '3470': ['0.448564593301435', '0.077529566360053', '0.00427807486631', '0', '0', '0'], '3475': ['0.450299401197605', '0.077176781002639', '0.004268943436499', '0', '0', '0'], '3480': ['0.45346062052506', '0.074538258575198', '0.004329004329004', '0', '0', '0'], '3485': ['0.457040572792363', '0.072655217965654', '0.004338394793926', '0', '0', '0'], '3490': ['0.460620525059666', '0.072089947089947', '0.002181025081788', '0', '0', '0'], '3495': ['0.462455303933254', '0.070720423000661', '0.002197802197802', '0', '0', '0'], '3500': ['0.464200477326969', '0.070152217074785', '0.002239641657335', '0', '0', '0'], '3505': ['0.466507177033493', '0.070140280561122', '0.002237136465324', '0', '0', '0'], '3510': ['0.468263473053892', '0.06951871657754', '0.002275312855518', '0', '0', '0'], '3515': ['0.47242206235012', '0.06769436997319', '0.002283105022831', '0', '0', '0'], '3520': ['0.475566150178784', '0.065084745762712', '0.002283105022831', '0', '0', '0'], '3525': ['0.48038049940547', '0.062158469945355', '0.002283105022831', '0', '0', '0'], '3530': ['0.480997624703088', '0.063282336578581', '0.001129943502825', '0', '0', '0'], '3535': ['0.481743227326266', '0.061397318278052', '0.001142857142857', '0', '0', '0'], '3540': ['0.48421052631579', '0.058739255014327', '0.001135073779796', '0', '0', '0'], '3545': ['0.487804878048781', '0.055596196049744', '0.001122334455668', '0', '0', '0'], '3550': ['0.490740740740741', '0.053333333333333', '0.001126126126126', '0', '0', '0'], '3555': ['0.497129735935706', '0.048484848484849', '0', '0', '0', '0'], '3560': ['0.507377979568672', '0.038910505836576', '0', '0', '0', '0'], '3565': ['0.511811023622047', '0.033680834001604', '0', '0', '0', '0'], '3570': ['0.51505016722408', '0.028665028665029', '0', '0', '0', '0'], '3575': ['0.517699115044248', '0.024513947590871', '0', '0', '0', '0'], '3580': ['0.520174482006543', '0.017361111111111', '0', '0', '0', '0'], '3585': ['0.522404371584699', '0.016903914590747', '0', '0', '0', '0'], '3590': ['0.524377031419285', '0.011915673693859', '0', '0', '0', '0'], '3595': ['0.530744336569579', '0.004708097928437', '0', '0', '0', '0'], '3600': ['0.536717062634989', '0', '0', '0', '0', '0'], '3605': ['0.536717062634989', '0', '0', '0', '0', '0'], '3610': ['0.537297297297297', '0', '0', '0', '0', '0'], '3615': ['0.540805223068553', '0', '0', '0', '0', '0'], '3620': ['0.546153846153846', '0', '0', '0', '0', '0'], '3625': ['0.553452115812918', '0', '0', '0', '0', '0'], '3630': ['0.557800224466891', '0', '0', '0', '0', '0'], '3635': ['0.560948081264108', '0', '0', '0', '0', '0'], '3640': ['0.561581920903955', '0', '0', '0', '0', '0'], '3645': ['0.562853907134768', '0', '0', '0', '0', '0'], '3650': ['0.565415244596132', '0', '0', '0', '0', '0'], '3655': ['0.574566473988439', '0', '0', '0', '0', '0'], '3660': ['0.577906976744186', '0', '0', '0', '0', '0'], '3665': ['0.580607476635514', '0', '0', '0', '0', '0'], '3670': ['0.587470449172577', '0', '0', '0', '0', '0'], '3675': ['0.590261282660333', '0', '0', '0', '0', '0'], '3680': ['0.594497607655502', '0', '0', '0', '0', '0'], '3685': ['0.600967351874244', '0', '0', '0', '0', '0'], '3690': ['0.603888213851762', '0', '0', '0', '0', '0'], '3695': ['0.606837606837607', '0', '0', '0', '0', '0'], '3700': ['0.61358024691358', '0', '0', '0', '0', '0'], '3705': ['0.61892901618929', '0', '0', '0', '0', '0'], '3710': ['0.624371859296482', '0', '0', '0', '0', '0'], '3715': ['0.626733921815889', '0', '0', '0', '0', '0'], '3720': ['0.630710659898477', '0', '0', '0', '0', '0'], '3725': ['0.636363636363636', '0', '0', '0', '0', '0'], '3730': ['0.640463917525773', '0', '0', '0', '0', '0'], '3735': ['0.64629388816645', '0', '0', '0', '0', '0'], '3740': ['0.649673202614379', '0', '0', '0', '0', '0'], '3745': ['0.653947368421053', '0', '0', '0', '0', '0'], '3750': ['0.660904255319149', '0', '0', '0', '0', '0'], '3755': ['0.663551401869159', '0', '0', '0', '0', '0'], '3760': ['0.668010752688172', '0', '0', '0', '0', '0'], '3765': ['0.677111716621253', '0', '0', '0', '0', '0'], '3770': ['0.684573002754821', '0', '0', '0', '0', '0'], '3775': ['0.692200557103064', '0', '0', '0', '0', '0'], '3780': ['0.69901547116737', '0', '0', '0', '0', '0'], '3785': ['0.704964539007092', '0', '0', '0', '0', '0'], '3790': ['0.712034383954155', '0', '0', '0', '0', '0'], '3795': ['0.719247467438495', '0', '0', '0', '0', '0'], '3800': ['0.724489795918367', '0', '0', '0', '0', '0'], '3805': ['0.730882352941176', '0', '0', '0', '0', '0'], '3810': ['0.734121122599705', '0', '0', '0', '0', '0'], '3815': ['0.737388724035608', '0', '0', '0', '0', '0'], '3820': ['0.744011976047904', '0', '0', '0', '0', '0'], '3825': ['0.749622926093514', '0', '0', '0', '0', '0'], '3830': ['0.758778625954198', '0', '0', '0', '0', '0'], '3835': ['0.762269938650307', '0', '0', '0', '0', '0'], '3840': ['0.768160741885626', '0', '0', '0', '0', '0'], '3845': ['0.774143302180685', '0', '0', '0', '0', '0'], '3850': ['0.778996865203762', '0', '0', '0', '0', '0'], '3855': ['0.788888888888889', '0', '0', '0', '0', '0'], '3860': ['0.79903536977492', '0', '0', '0', '0', '0'], '3865': ['0.805510534846029', '0', '0', '0', '0', '0'], '3870': ['0.81342062193126', '0', '0', '0', '0', '0'], '3875': ['0.82013201320132', '0', '0', '0', '0', '0'], '3880': ['0.829716193656093', '0', '0', '0', '0', '0'], '3885': ['0.840947546531303', '0', '0', '0', '0', '0'], '3890': ['0.845238095238095', '0', '0', '0', '0', '0'], '3895': ['0.858376511226252', '0', '0', '0', '0', '0'], '3900': ['0.864347826086956', '0', '0', '0', '0', '0']}
    
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
    if(scorebot.isD1(hTeam,hTeam,'Men') or hTeam in chnDiffs.keys()):
        if(hTeam in chnDiffs.keys()):       
            hTeam=chnDiffs[hTeam]
    
    if(scorebot.isD1(aTeam,aTeam,'Men') or aTeam in chnDiffs.keys()):
        if(aTeam in chnDiffs.keys()):       
            aTeam=chnDiffs[aTeam]
            
    url = "https://www.collegehockeynews.com/ratings/krach.php"
    url = "https://www.collegehockeynews.com/ratings/krach/2019" #TODO Remove
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
            return "Tie {}%".format(round(tiedProb*100,1))
    
    if(hScore>aScore):
        
        winProb = float(winLookup[str(secTime)][gd])
        return "{} {}%".format(hTeam,round(hOdds*(1-secTime/3600)+winProb*100,1))
    
    if(aScore>aScore):
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
    parser.feed(html.decode("utf-8"))
    
    if("<meta HTTP-EQUIV=\"REFRESH\"" in html.decode("utf-8")):
        html = html.decode("utf-8")
        url=html.split("url=")
        url=url[1].split("\"")[0]
        f=urllib.request.urlopen(url,timeout = 10)
        html = f.read()
        f.close()
        parser.feed(html.decode("utf-8"))
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
    newha =['Saint Anselm','Franklin Pierce',"Saint Michael's"]      
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
                        print(i)
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
            await message.channel.send("https://m.imgur.com/ZPZUGW0")
            
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
        "liu" : "Long Island",
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
    parser.feed(html.decode("utf-8"))
    
    if("<meta HTTP-EQUIV=\"REFRESH\"" in html.decode("utf-8")):
        html = html.decode("utf-8")
        url=html.split("url=")
        url=url[1].split("\"")[0]
        f=urllib.request.urlopen(url,timeout = 10)
        html = f.read()
        f.close()
        parser.feed(html.decode("utf-8"))
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

client.run(TOKEN)
print("Ending... at",datetime.datetime.now())
