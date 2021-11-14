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
import matplotlib.pyplot as plt
import numpy as np
import imageio
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
season = '2122'
invalidRoles = ['@everyone', 'Mods', 'Admin', 'bot witch', 'Dyno', 'CH_Scorebot']

chnDiffs={"Minnesota Duluth":"Minnesota-Duluth",
    "Lake Superior State" : "Lake Superior",
    "UMass Lowell" : "Mass.-Lowell",
    "American International" : "American Int'l",
    "Army West Point" : "Army",
    "Alabama Huntsville" : "Alabama-Huntsville",
    "Alaska Anchorage" : "Alaska-Anchorage",
    "UConn" : "Connecticut",
    "Long Island University": "Long Island",
    "St Thomas" : "St. Thomas"}

flairlist = {"American International" : "<:aic:693220791076126760>",
"Air Force" : "<:airforce:761701456188538890>",
"Alaska" : "<:alaska:761701457077600266>",
"Army West Point" : "<:army:761701458311381003>",
"Arizona State" : "<:asu:761701459200704532>",
"Boston College" : "<:bc:666831654727188481>",
"Bemidji State" : "<:bemidji:684982886956400658>",
"Bentley" : "<:bentley:761701460143505428>",
"Brown" : "<:brown:761701499092598817>",
"Boston University" : "<:bu:666832026095321088>",
"Bowling Green" : "<:bgsu:762019455358206002>",
"Canisius" : "<:canisius:761701535985565747>",
"Clarkson" : "<:clarkson:666834128834134017>",
"Colgate" : "<:colgate:791441084420980746>",
"Colorado College" : "<:coloradocollege:761701485821689858>",
"Cornell" : "<:cornell:666832546033827892>",
"Dartmouth" : "<:dartmouth:761701466876280893>",
"Denver" : "<:denver:666833535616679967>",
"Ferris State" : "<:ferrisstate:761701516696092702>",
"Franklin Pierce" : "<:franklinpierce:761701546223599657>",
"Harvard" : "<:harvard:666834657681342474>",
"Holy Cross" : "<:holycross:761701495673585705>",
"Lake Superior State" : "<:lakesuperior:761701538661400616>",
"Lindenwood" : "<:lindenwood:761701500426649640>",
"Long Island University" : "<:liu:761701500565061655>",
"UMass Lowell" : "<:lowell:761701500397158450>",
"Maine" : "<:maine:761701510668615730>",
"Minnesota State" : "<:mankato:666832880475045900>",
"Mercyhurst" : "<:mercyhurst:761701538425995286>",
"Merrimack" : "<:merrimack:761701513541189692>",
"Miami" : "<:miami:761701476619386910>",
"Michigan" : "<:michigan:761701476603002900>",
"Michigan Tech" : "<:michigantech:761701513663742022>",
"Michigan State" : "<:michiganstate:761734569871147039>",
"Minnesota" : "<:minnesota:666834959142617088>",
"Niagara" : "<:niagara:761701505681457162>",
"North Dakota" : "<:northdakota:666836576675823628>",
"Northeastern" : "<:northeastern:666837132488474675>",
"Northern Michigan" : "<:northernmichigan:761701501642866689>",
"Notre Dame" : "<:notredame:761701477407522846>",
"Ohio State" : "<:ohiostate:666832702661459968>",
"Omaha" : "<:omaha:761701489047371807>",
"Penn State" : "<:pennstate:761701497728794665>",
"Post" : "<:post:761701537881260043>",
"Princeton" : "<:princeton:666835295194316810>",
"Providence" : "<:providence:666837749428387850>",
"Quinnipiac" : "<:quinnipiac:676508163419406357>",
"RIT" : "<:rit:761701547276632099>",
"Robert Morris" : "<:robertmorris:761701542360383518>",
"Rensselaer" : "<:rpi:761701489587912744>",
"Sacred Heart" : "<:sacredheart:761701502100176908>",
"St. Cloud State" : "<:scsu:761701498178502689>",
"Saint Anselm" : "<:stanselm:761701537214889994>",
"St. Lawrence" : "<:stlawrence:761701547754389514>",
"Saint Michael's" : "<:stmichaels:761701516331450368>",
"Stonehill " : "<:stonehill:761701509595136060>",
"St. Thomas" : "<:stthomas:761701532261154856>",
"Syracuse" : "<:syracuse:761701481384509460>",
"Alabama Huntsville" : "<:uah:716027231700516895>",
"Alaska Anchorage" : "<:uaa:761701504376766464>",
"UConn" : "<:uconn:761701507782934548>",
"Massachusetts" : "<:umass:666832224783695879>",
"Minnesota Duluth" : "<:umd:666836078019215360>",
"New Hampshire" : "<:unh:761701513236054027>",
"Union" : "<:union:761701482030039070>",
"Vermont" : "<:vermont:761701504691339274>",
"Western Michigan" : "<:wmu:849722307446571018>",
"Wisconsin" : "<:wisconsin:666834959897722900>",
"Yale" : "<:yale:761701482352607272>",
"Minnesota-Duluth": "<:umd:666836078019215360>",
"Lake Superior" : "<:lakesuperior:761701538661400616>",
"Long Island" : "<:liu:761701500565061655>",
"Mass.-Lowell" : "<:lowell:761701500397158450>",
"Nebraska-Omaha": "<:omaha:761701489047371807>",
"American Int'l": "<:aic:693220791076126760>",
"Army": "<:army:761701458311381003>",
"Alabama-Huntsville": "<:uah:716027231700516895>",
"Alaska-Anchorage" : "<:uaa:761701504376766464>",
"Connecticut" : "<:uconn:761701507782934548>"}

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
    helpStr = ['''
?[mscore / wscore] [team name] - current scoreline for Current Men's/Women's game of team entered
?[mstand / wstand] [conference name] - current standings for conference entered
?[cheer / jeer / boo] [team name] - sends random cheers for / jeers against team entered (Suggestions welcome in #suggestion-box)
?[cheer] - cheers for team of user's flair color
?[pwr / krach] - displays current Top 16 Pairwise Ranking / KRACH
?[pwr / krach] top - displays current Top 4 Pairwise Ranking / KRACH
?[pwr / krach] bottom - displays current Bottom 5 Pairwise Ranking / KRACH
?[pwr / krach] bubble - displays the Pairwise Ranking Bubble / KRACH
?[pwr / krach] <number> - displays Top <number\> Pairwise Ranking / KRACH
?[pwr / krach] <number>,<number2> - displays <number\> to <number2\> Pairwise Ranking / KRACH
?[wpwr / wkrach] - displays current Top 8 Pairwise Ranking / KRACH
?[wpwr / wkrach] top - displays current Top 4 Pairwise Ranking / KRACH
?[wpwr / wkrach] bottom - displays current Bottom 5 Pairwise Ranking / KRACH
?[wpwr / wkrach] bubble - displays the Pairwise Ranking Bubble / KRACH
?[wpwr / wkrach] <number> - displays Top <number> Pairwise Ranking / KRACH
?[wpwr / wkrach] <number>,<number2> - displays <number\> to <number2\> Pairwise Ranking / KRACH
?[wpwr / wkrach] [team name] - displays Pairwise Ranking of team entered plus 2 teams above and 2 teams below
?[pwc] [team1],[team2] - display Pairwise Comparison between two teams
    ''',
    '''
?[odds / wodds] [team1],[team2] - displays KRACH computed odds of winning the matchup
?[odds3 / wodds3] [team1],[team2] - displays KRACH computed odds of winning best of three matchup
?[msched / wsched] [team] - displays next 5 games of the team entered (All Caps denotes [team] is home)
?[msched / wsched] [team],<number> - displays next <number> games of the team entered (All Caps denotes [team] is home)
?[msched / wsched] [team],[team2] - displays results and head to head schedule of teams entered (All Caps denotes [team] is home)
?[mstats / wstats] [team],[player name/number] - displays player stats of given player
?[mres / wres / mform / wform] [team name] - displays previous 5 games of the team entered (All Caps denotes [team] is home)
?[mres / wres / mform / wform] [team],<number> - displays previous <number> games of the team entered (All Caps denotes [team] is home)
?[history] [team1],[team2] - displays Matchup history and recent results
?[history] [team1],[team2],<number> - displays Matchup history and recent results
?[whatsontv] - displays list of Today's games broadcasted on TV
?[pdoplot] - displays PDO plot (note may take a few minutes to generate)
?[corsi] - displays PDO plot (note may take a few minutes to generate)
?[chain/whosbetter] [team1],[team2] - displays transitive win chain from team 1 to team 2 
?[thanksbot] - Thanks Bot
?[roles] - display list of available roles
?[roles] [role/team name] - adds role to user
?[rroles] [role/team name] - removes role from user
?[dog] - displays random dog pic
?[cat] - displays random cat pic

Scores/Standings/TV Listings/Stats courtesy of collegehockeynews.com
Pairwise Rankings courtesy of collegehockeynews.com
Women's Pairwise Rankings courtesy of uscho.com
Women's KRACH calculations courtesy of lugnut92
Cheers/Jeers courtesy of Student Sections across America
Bot courtesy of redsoxfan2194
    ''']
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
                "Craig" : "Craig",
                "Voter" : "/r/collegehockey Poll Voter",
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
                "St. Thomas" : "St. Thomas Tommies",
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
    elif(role == "color wisconsin"):
        role = "Wisconsin Badgers"
    elif(role == "color north dakota"):
        role = "North Dakota Fighting Hawks"
    cheerList = { "Boston University Terriers" : ["Go BU!", "Let's Go Terriers!", "BC Sucks!"],
    "Northeastern Huskies" : ["Go NU!", "#HowlinHuskies", "Go Huskies!"],
    "Cornell Big Red" : ["Let's Go Red!", "Go Big Red!", "Fuck Harvard!", "Screw BU!"],
    "Harvard Crimson" : ["Go Harvard!", "Fuck Harvard!"],
    "New Hampshire Wildcats" : ["I Believe in UNH!","Go Wildcats!"],
    "Maine Black Bears" : ["Let's go Black Bears!", "Fill the steins to Dear Ol' Maine!"],
    "Boston College Eagles" : ["Go BC!", "BC Sucks!", "Go Eagles!", "Sucks to BU!"],
    "UMass Minutemen" : ["Go Amherst!", "Go U Mass!"],
    "UConn Huskies" : ["Go Huskies!", "U-C-O-N-N UCONN UCONN UCONN", "Ice Bus"],
    "Union Dutchmen/Dutchwomen" : ["Let's Go U!"],
    "Michigan Tech Huskies" : ["Go Huskies!"],
    "UMass Lowell River Hawks" : ["Go River Hawks!"],
    "Lake Superior State Lakers" : ["Ringy Dingy!"],
    "Bemidji State Beavers" : ["Roll Beaves!", "Go Beaves!", "Go Beavers!"],
    "Omaha Mavericks" : ["Everyone for Omaha!"],
    "Clarkson Golden Knights" : ["Let's Go Tech!"],
    "Vermont Catamounts" : ["Go Catamounts!"],
    "Penn State Nittany Lions" : ["We Are!", "Hockey Valley! Clap clap clapclapclap"],
    "Minnesota Golden Gophers" : ["Go Gophers!"],
    "Michigan Wolverines": ["Go Blue!"],
    "Michigan State Spartans" : ["Go Sparty!", "Go Green!"],
    "North Dakota Fighting Hawks" : ["Go Hawks!"],
    "Sieve": ["Sieve, You Suck!", "Sieve! Sieve! Sieve! Sieve!", "It's All Your Fault!"],
    "RPI Engineers" : ["Let's Go Red!", "Go Red!\nGo White!"],
    "RIT Tigers" : ["Go Tigers!"],
    "Notre Dame Fighting Irish" : ["Go Irish!"],
    "Providence Friars" : ["Go Friars!"],
    "St. Cloud State Huskies" : ["Go Huskies!"],
    "Minnesota State Mavericks" : ["Go Mavericks!"],
    "Minnesota Duluth Bulldogs" : ["Go Bulldogs!"],
    "Quinnipiac Bobcats" : ["Go Bobcats!", "Meowwww", "Feed. The. Kitty."],
    "Denver Pioneers" : ["Let's Go DU!", "Go Pios!"],
    "Ohio State Buckeyes" : ["Go Buckeyes!", "O-H!"],
    "Arizona State Sun Devils" : ["Forks Up!","Go Sparky!"],
    "Bowling Green Falcons" : ["Ay Ziggy", "Go Ziggy!"],
    "Brown Bears" : ["Go Bruno!"],
    "Yale Bulldogs" : ["Boola Boola"],
    "Wisconsin Badgers" : ["On Wisconsin!"],
    "Merrimack Warriors" : ["Macktion!", "Go Warriors!", "Go Mack!"],
    "Colgate Raiders" : ["Go Gate!"],
    "Colorado College Tigers" : ["Go Tigers! DU still sucks!"],
    "Holy Cross Crusaders" : ["Go Cross Go"],
    "Army Black Knights" : ["Go Army! Beat Navy!"],
    "Alabama Huntsville Chargers" : ["STAN HORSIES!!", "Go Chargers!", "Go Big Blue!"],
    "LIU Sharks" : ["Go Sharks!", "Here we go Sharks!", "Strong Island"],
    "Northern Michigan Wildcats" : ["Go 'Cats, Go 'Cats, Go 'Cats, GO!", " Tech Still Sucks!"],
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
    elif(role == "color maine"):
        role = "Maine Black Bears"
    elif(role == "color wisconsin"):
        role = "Wisconsin Badgers"
    elif(role == "color north dakota"):
        role = "North Dakota Fighting Hawks"
    jeerList = { "Boston College Eagles" : ["BC Sucks!", "Fuck 'Em Up! Fuck 'Em Up! BC Sucks!", "Sunday School!", "Not From Boston!" ,"```\nFor Newton, For Newton\nThe Outhouse on the hill!\nFor Newton, For Newton\nBC sucks and always will!\nSo here’s to the outhouse on the hill,\nCause Boston College sucks and they always will,\nFor Newton, For Newton,\nThe outhouse on the hill!```"],
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
    "Cornell Big Red" : ["Harvard Rejects!", "```\nUp above Cayuga's waters, there's an awful smell;\nThirty thousand Harvard rejects call themselves Cornell.\nFlush the toilet, flush the toilet,\nFlush them all to hell!\nThirty thousand Harvard rejects call themselves Cornell!```"],
    "Maine Black Bears" : ["M-A-I-N-E ~~Go Blue~~ MAAAAAIIINNNE SUCKS", "UMOwO"],
    "Louisiana State University Tigers" :["Louisiana State University and Agricultural and Mechanical College"],
    "Wisconsin Badgers" : ["Dirty Sconnies", "https://i.imgur.com/sljug4m.jpg"],
    "Michigan State Spartans" : ["Poor Sparty"],
    "Michigan Wolverines" : ["```\nO, we don't give a damn for the whole state of Michigan\nThe whole state of Michigan, the whole state of Michigan\nWe don't give a damn for the whole state of Michigan, we're from Ohio\nWe're from Ohio...O-H\nWe're from Ohio...I-O\nO, we don't give a damn for the whole state of Michigan\nThe whole state of Michigan, the whole state of Michigan\nWe don't give a damn for the whole state of Michigan, we're from Ohio```"],
    "Notre Dame Fighting Irish" : ["Blinded by the Light", "Notre Lame!", "Rudy was offsides!", "https://youtu.be/OCbuRA_D3KU"],
    "St. Cloud State Huskies" : ["Go back to Montreal!", "St. Cloud Sucks!", "St. Cloud is not a state"],
    "RPI Engineers" : ["KRACH is Better!"],
    "Minnesota State Mavericks" : ["Mankatno", "Mankato Sucks!"],
    "Minnesota Duluth Bulldogs" : ["Duluth Sucks!"],
    "Minnesota Golden Gophers" : ["Golden Goofs"],
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
    "Holy Cross Crusaders" : ["Boo Cross Boo", "Holy Cow", "No Cross No", "Moo Cow Moo"],
    "Army Black Knights" : ["Woops", "Ring Knockers", "https://www.dictionary.com/e/slang/circle-game/"],
    "Air Force Falcons" : ["Ring Knockers", "Chair Force"],
    "LIU Sharks" : ["Baby Shark Doo doo, doo doo doo doo"],
    "Sieve": ["Sieve, You Suck!", "Sieve! Sieve! Sieve! Sieve!", "It's All Your Fault!"],
    "Craig" : ["Imagine being named Craig"],
    "Yankees" : ["Yankees Suck!"],
    "Ref": ["I'm Blind! I'm Deaf! I wanna be a ref!", "Hey Ref, check your phone, you missed a few calls.", "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", ":regional_indicator_b: :regional_indicator_u: :regional_indicator_l: :regional_indicator_l: :regional_indicator_s: :regional_indicator_h: :regional_indicator_i: :regional_indicator_t:"]}
    if role in jeerList:
            return random.choice(jeerList[role])
    else:
        return "";
 
def getPairwise(opt):
    global chnDiffs
    #return "Pairwise is currently unavailable for the 2020-21 Season, use ?mpwr for an approximation"
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

    teams = []
    start = 0
    splitopt = opt.split(',')

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
        
    elif(len(splitopt)==2):
        if(splitopt[0].isnumeric() and splitopt[1].isnumeric()):
            sOpt=int(splitopt[0])
            eOpt=int(splitopt[1])
            if(sOpt>0):
                start=sOpt-1
            else:
                start=0
                
            if(eOpt<=60):
                end = eOpt
            else:
                end=60
            
            if(sOpt>eOpt):
                swap=start
                start=end-1
                end=swap+1
            
    else:
        end = 16
    
    if(len(pairwise)<end):
        end=len(pairwise)
        
    rankings = "```\n"
        
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,pairwise[i])
    rankings += "```"
    return rankings
def getKRACH(opt):
    global chnDiffs
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

    teams = []
    start = 0
    splitopt = opt.split(',')
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
    elif(len(splitopt)==2):
        if(splitopt[0].isnumeric() and splitopt[1].isnumeric()):
            sOpt=int(splitopt[0])
            eOpt=int(splitopt[1])
            if(sOpt>0):
                start=sOpt-1
            else:
                start=0
                
            if(eOpt<=60):
                end = eOpt
            else:
                end=60
            
            if(sOpt>eOpt):
                swap=start
                start=end-1
                end=swap+1
    else:
        end = 16

    rankings = "```\n"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,krach[i])
    rankings += "```"
    return rankings
    
def getMatchupHistory(team,opp,numGames):
    global chnDiffs
    minSeason=19001901
    maxSeason=20212022
    if(numGames.isnumeric()):
        numGames=int(numGames)
        if(numGames>15):
            numGames=15
    else:
        numGames=5
    if(team == '' or opp == ''):
        
        return "Enter Two Teams!"
        
    team = decodeTeam(team)
    opp = decodeTeam(opp)
    if(scorebot.isD1(team,team,'Men') or team in chnDiffs.keys()):
        if(team in chnDiffs.keys()):       
            team=chnDiffs[team]
    else:
        
        return "Team 1 Not Found"

    if(scorebot.isD1(opp,opp,'Men') or opp in chnDiffs.keys()):
        if(opp in chnDiffs.keys()):       
            opp=chnDiffs[opp]
    else:
        
        return "Team 2 Not Found"
    if(team == opp):
        
        return "Enter Two Different Teams!"

    team=team.replace('.','')
    opp=opp.replace('.','')
    '''
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
            hrefDict[link.get_text()]=idNum
    #print(hrefDict)
    '''
    url = "https://www.collegehockeynews.com/reports/teamindex-historical.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    pairwise = []
    hrefDict = {}
    for link in soup.find_all('a',{'class':'team'}):
            #print(link['href'],repr(link.get_text()),repr(opp))
            #print(link['href'])
            res=re.search('.*\/(.*)\/(\d*)',link['href'])
            idNum=res.group(2)
            teamName=res.group(1)
            teamName=teamName.replace('-',' ')
            hrefDict[teamName]=idNum
   
    url = "https://www.collegehockeynews.com/schedules/?search=1&field[year_min]={}&field[year_max]={}&field[teamID]={}&field[oppID]={}".format(minSeason,maxSeason,hrefDict[team],hrefDict[opp])
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    tab = soup.find("table",{"class":"data schedule full"})
    games=tab.findChildren('tr');
    matchupData = {};
    gNum = 0
    
    gameHistory = "" 
    for game in games:
        gameStr=game.findChildren('td')[0].get_text()
        gameStr=gameStr.replace(u'\xa0',u'')
        gameStr=gameStr.replace('*',u'')
        gameStr=gameStr.replace('Box',u'')
        gameStr=gameStr.replace('\n',u'!')
        gameStr=gameStr.replace('\t',u'!')
        gameStr=gameStr.replace('!!!',u'')
        gameStr=gameStr.replace('!!',u'!')
        
        gameData=gameStr.split('!')
       # print(gameData)
        gameData.pop()

        if(gameData!=[]):
            date=gameData[0]
            aTeam=gameData[1]
            aScore=int(gameData[2])
            hTeam=gameData[4]
            hScoreTemp = gameData[5].split(' ')
            hScore=int(hScoreTemp[0])
            if(len(gameData)>=7):
                if('ot' in gameData[6]):
                    loc=gameData[6]
                else:
                    loc=''
            else:
                loc=''
            if(aScore>hScore):
              winner=aTeam
              wScore=aScore
              lScore=hScore
            elif(hScore>aScore):
              winner=hTeam
              wScore=hScore
              lScore=aScore
            else:
              winner='Tie'
              wScore=hScore
              lScore=aScore
            gNum+=1
            matchupData[gNum]={'Date': date, 'awayTeam':aTeam, 'awayScore': aScore, 'homeTeam':hTeam,'homeScore':hScore, 'Location':loc,'Winner': winner,'winnerScore':wScore,'loserScore':lScore}
           
            if(gNum<=numGames):
                #return
               # gameHistory+="{} {} {} {} {} {}\n".format(matchupData[gNum]['Date'],matchupData[gNum]['awayTeam'],matchupData[gNum]['awayScore'],matchupData[gNum]['homeTeam'],matchupData[gNum]['homeScore'],matchupData[gNum]['Location'])
               gameHistory+="{} {} {}-{} {}\n".format(matchupData[gNum]['Date'],matchupData[gNum]['Winner'],matchupData[gNum]['winnerScore'],matchupData[gNum]['loserScore'],matchupData[gNum]['Location'])
    
    if(gNum>0):
        gameHistory = "Recent Results:\n" + gameHistory
        
    teamWins=0
    oppWins=0
    ties=0
    leader='Tied'
    for i in matchupData.keys():
        matchupData[i]['Winner'] = matchupData[i]['Winner'].replace('-',' ')
        matchupData[i]['Winner'] = matchupData[i]['Winner'].replace('.','')
        matchupData[i]['Winner'] = matchupData[i]['Winner'].replace("'",'')
        if(matchupData[i]['Winner']==team):
            teamWins+=1
        elif(matchupData[i]['Winner']==opp):
            oppWins+=1
        else:
            ties+=1
    if(teamWins>oppWins):
       leader = '{} Leads'.format(team)
    elif(oppWins>teamWins):
       leader = '{} Leads'.format(opp)
       
    allTimeRecord = "All-Time Series: \n{} {}-{}-{}".format(leader, teamWins,oppWins,ties)
    historyData = "```\n{} v {}\n\n{}\n\n{}```".format(team,opp,allTimeRecord,gameHistory)
    
    return historyData
    
def getWinProb(aTeam, aScore, hTeam, hScore, status):
    global chnDiffs

    if('Final' in status):
        return ''
      
    return ''

        
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
    
    global chnDiffs
        
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
        if(line and 'RRWP' not in line and 'Ratio' not in line and 'Strength' not in line and 'Winning' not in line):
            line=line.rstrip('!')
            line=line.split("!")
            if(line[2]=='∞'):
                line[2] = "inf"
            krach[line[1]]=float(line[2])
    
    team1Odds = krach[team1]/(krach[team1]+krach[team2])
    team2Odds = krach[team2]/(krach[team1]+krach[team2])
    
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))

def getKOdds3(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
    global chnDiffs
       
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
            if(line[2]=='∞'):
                line[2] = "inf"
            krach[line[1]]=float(line[2])
    
    team1Odds = (krach[team1]**2 * (krach[team1] + 3 * krach[team2]))/((krach[team1] + krach[team2])**3)
    team2Odds = (krach[team2]**2 * (krach[team2] + 3 * krach[team1]))/((krach[team2] + krach[team1])**3)
    
    
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))

def getPWRComp(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
    
    global chnDiffs
 
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
    pwrComp = '```\n'
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
        gender='reports'
        if(conf=="hea" or conf == "he" or conf == 'hockeyeast'):
            conference = 4
        elif(conf == "ivy"):
            conference = 3
        elif(conf == "atlantic" or conf == "ahc" or conf == "aha"):
            conference = 0
        elif(conf == "bigten" or conf == "b10" or conf == "b1g" or conf == "big10" ):
            conference = 1
        elif(conf == "nchc"):
            conference = 5
        elif(conf == "ccha"):
            conference = 2
        elif(conf == "ecac"):
            conference = 3
        elif(conf == "ind" or conf == "independent"):
            conference = 6
        else:
            return "I don't know that conference."
    elif(m_w == "Women"):
        gender='women'
        if(conf=="hea" or conf == "he" or conf == 'hockeyeast'):
            conference = 1
        elif(conf == "ivy"):
            conference = 0
        elif(conf == "cha"):
            conference = 3
        elif(conf == "wcha"):
            conference = 2
        elif(conf == "ecac"):
            conference = 0
        elif(conf == "newha"):
            conference = 4
        else:
            return "I don't know that conference."
    else:
        return "I don't know that conference."

    url = "https://www.collegehockeynews.com/{}/standings.php".format(gender)
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    confTab= soup.find_all('table')
    
    rows=confTab[conference].find('tbody').find_all('tr')
    standings="```\n"
    standings+= "{: <30}Conference\t\tOverall\n".format('')
    standings+="{: <18}  Pts  GP  RW  RL  OW  OL | GP  W  L  T  OW  OL  GF  GA\n".format('')

    for row in rows:
        team=[]
        for i in row.find_all('td'):
              team.append(i.get_text())
        team[1]="{: <18}".format(team[1])
        if(team[7]==''):
            team[7]='0'
        if(team[8]==''):
            team[8]='0'
        if(team[17]==''):
            team[17]='0'
        if(team[18]==''):
            team[18]='0'
        standings+="{:<2} {:}{:<2}  {:<2}  {:<2}  {:<2}  {:<2}  {:<2} |  {:<2} {:<2} {:<2} {:<2}  {:<2}  {:<2} {:<2} {:<2}\n".format(team[0],team[1],team[3],team[2],team[5],team[6],team[7],team[8],team[10], team[11],team[12],team[13],team[17],team[18],team[19],team[20])

    standings += "```"
    return standings
        
    
def getGamesOnTV():
    gameList = []
    for gender in ["Men","Women"]:
        if gender=='Men':
            url = "https://www.collegehockeynews.com/schedules/scoreboard.php"
        elif gender == 'Women':
            url = "https://www.collegehockeynews.com/women/scoreboard.php"
            
        f=urllib.request.urlopen(url,timeout=10)
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'html.parser')
        data =soup.find_all('div',{'class':'confGroup'})
        nextbutton = soup.find('a',{'class':'button2 next'})
        now = datetime.datetime.now()
        
        if(nextbutton.get_text() == 'Today' and now.hour>4):
            url = "https://www.collegehockeynews.com/{}".format(nextbutton['href'])
            f=urllib.request.urlopen(url,timeout=10)
            html = f.read()
            f.close()
            soup = BeautifulSoup(html, 'html.parser')
            data =soup.find_all('div',{'class':'confGroup'})
           
        
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

            gCount=0
            for i in games:
                if(tvList[gCount]!=' '):
                    gameData=i.find_all('td')
                    
                    if(len(gameData)>=8):
                        awayTeam=gameData[2].get_text()
                        awayScore=gameData[3].get_text()
                        homeTeam=gameData[7].get_text()
                        homeScore=gameData[8].get_text()
                        status=gameData[4].get_text(separator=" ")
                    elif(len(gameData)==7):
                        awayTeam=gameData[1].get_text()
                        awayScore=gameData[2].get_text()
                        homeTeam=gameData[5].get_text()
                        homeScore=gameData[6].get_text()
                        status=gameData[3].get_text(separator=" ")
                        
                    gameDict = {'awayTeam' : awayTeam,
                        'awayScore': "",
                        'homeTeam' : homeTeam,
                        'homeScore': "",
                        'league' : conference,
                        'startTime': status,
                        'status' : status,
                        'm_w': gender,
                        'channel' : tvList[gCount].rstrip(' ')}
                        
                    gameList.append(gameDict)
                gCount+=1
    tvGames = ""
    for game in gameList:
        if(game['channel'] != ''):
            if("a.m." not in game['status'] and "p.m." not in game['status']):
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
    
    url = "https://json-b.uscho.com/json/rankings/pairwise-rankings/d-i-women"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    site_json=json.loads(soup.text)
    table=site_json['json']['dt1']['data']
    pwr=[]
    for row in table:
        pwr.append(row[1])
        
    start = 0
    splitopt = opt.split(',')
    decodedTeam = decodeTeam(opt)
    if(opt.isnumeric()):
        end = int(opt)
    elif(opt.lower()=='full'):
        end = 41
    elif(scorebot.isD1(decodedTeam,decodedTeam,'Women')):
        if(decodeTeam=='UConn'):
            decodedTeam='Connecticut'
        teamIdx=pwr.index(decodedTeam)
        if(teamIdx-2<0):
            start=0
        else:
            start = teamIdx-2
        if(teamIdx+3>41):
            end=41
        else:
            end = teamIdx+3
    elif(opt.lower() == 'bubble'):
        start = 5
        end = 12
    elif(opt.lower() == 'top'):
        end = 4
    elif(opt.lower() == 'bottom'):
        start = 35
        end = 41
    elif(len(splitopt)==2):
        if(splitopt[0].isnumeric() and splitopt[1].isnumeric()):
            sOpt=int(splitopt[0])
            eOpt=int(splitopt[1])
            if(sOpt>0):
                start=sOpt-1
            else:
                start=0
                
            if(eOpt<=41):
                end = eOpt
            else:
                end=41
            
            if(sOpt>eOpt):
                swap=start
                start=end-1
                end=swap+1
    else:
        end = 8
    rankings = "```\n"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,pwr[i])
    rankings += "```"
    return rankings
        
def getWKRACH(opt):
    return "Women's KRACH Currently Unavailable"
    global teamDict,season
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
                elif(game.count('5OT')>0):
                    numOT = '5OT'
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
                game[4] = game[4].replace(' 2OT','')
                game[4] = game[4].replace(' 3OT','')
                game[4] = game[4].replace(' 4OT','')
                game[4] = game[4].replace(' 5OT','')
                pwrGameDict = {'awayTeam' : game[0],
                            'awayScore': game[1],
                            'homeTeam' : game[3],
                            'homeScore': game[4]}
                if(game[5]=='EX' or not scorebot.isD1(pwrGameDict['homeTeam'],pwrGameDict['homeTeam'],'Women') or not scorebot.isD1(pwrGameDict['awayTeam'],pwrGameDict['awayTeam'],'Women')):
                    continue
                if(pwrGameDict['homeTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['homeTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0 ,'teamsPlayed': [], "Rating" : 100}})
                if(pwrGameDict['awayTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['awayTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0, 'teamsPlayed': [], "Rating" : 100}})
                
                
                if(int(pwrGameDict['homeScore']) > int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Wins'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Losses'].append(pwrGameDict['homeTeam'])
                    
                elif(int(pwrGameDict['homeScore']) == int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Ties'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Ties'].append(pwrGameDict['homeTeam'])
                else:
                    teamDict[pwrGameDict['homeTeam']]['Losses'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Wins'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['teamsPlayed'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['teamsPlayed'].append(pwrGameDict['awayTeam'])  
                

    for team in teamDict.keys():
        teamDict[team]['Ratio'] = (len(teamDict[team]["Wins"])+len(teamDict[team]["Ties"])*.5)/(len(teamDict[team]["Losses"])+len(teamDict[team]["Ties"])*.5)

    converged = False
    while(not converged):
        for team in teamDict.keys():
            tWFactor = 0
            sumKrach = 0
            for oppo in set(teamDict[team]['teamsPlayed']):
                sumKrach += (teamDict[team]['Rating']*teamDict[team]['teamsPlayed'].count(oppo))/(teamDict[team]['Rating']+teamDict[oppo]['Rating'])
            newRating = ((len(teamDict[team]['Wins'])+len(teamDict[team]['Ties'])*.5)/sumKrach)*teamDict[team]['Rating']
            ratio = math.fabs(1-(newRating/ teamDict[team]['Rating']))

            if(ratio <= 0.00001):
                converged=True
            teamDict[team]['Rating']= newRating
        if(converged):
            break

    for i in range(10):
        scale_wins = 0
        for team in teamDict.keys():
            scale_wins += 100/(100 + teamDict[team]['Rating'])
        scale = scale_wins/20
        
        for team in teamDict.keys():
            teamDict[team]['Rating'] *= scale

    krachDict ={}
    for i in teamDict.keys():
        if(scorebot.isD1(i,i,'Women')):
            krachDict[i] = teamDict[i]['Rating']
        
    sorted_krach = sorted(krachDict.items(), key=operator.itemgetter(1), reverse=True)
    krach = []
    for i in sorted_krach:
        krach.append(i[0])
    start = 0
    splitopt = opt.split(',')
    decodedTeam = decodeTeam(opt)
    if(opt.isnumeric()):
        end = int(opt)
    elif(opt.lower()=='full'):
        end = 41
    elif(scorebot.isD1(decodedTeam,decodedTeam,'Women')):

        teamIdx=krach.index(decodedTeam)
        if(teamIdx-2<0):
            start=0
        else:
            start = teamIdx-2
        if(teamIdx+3>41):
            end=41
        else:
            end = teamIdx+3
    elif(opt.lower() == 'bubble'):
        start = 5
        end = 12
    elif(opt.lower() == 'top'):
        end = 4
    elif(opt.lower() == 'bottom'):
        start = 35
        end = 41
    elif(len(splitopt)==2):
        if(splitopt[0].isnumeric() and splitopt[1].isnumeric()):
            sOpt=int(splitopt[0])
            eOpt=int(splitopt[1])
            if(sOpt>0):
                start=sOpt-1
            else:
                start=0
                
            if(eOpt<=41):
                end = eOpt
            else:
                end=41
            
            if(sOpt>eOpt):
                swap=start
                start=end-1
                end=swap+1   
    else:
        end = 8
    rankings = "```\n"
    for i in range(start,end):
        rankings+="{}. {}\n".format(i+1,krach[i])
    rankings += "```"
    return rankings

def getWOdds(team1,team2):
    
    global teamDict,season
    url = "http://www.collegehockeystats.net/{}/schedules/ncw".format(season)
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"                
        
    team1 = decodeTeam(team1)
    team2 = decodeTeam(team2)
    if(not scorebot.isD1(team1,team1,'Women')):
        return "Team 1 Not Found"
    
    if(not scorebot.isD1(team2,team2,'Women')):
        return "Team 2 Not Found"
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
                elif(game.count('5OT')>0):
                    numOT = '5OT'
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
                game[4] = game[4].replace(' 2OT','')
                game[4] = game[4].replace(' 3OT','')
                game[4] = game[4].replace(' 4OT','')
                game[4] = game[4].replace(' 5OT','')
                pwrGameDict = {'awayTeam' : game[0],
                            'awayScore': game[1],
                            'homeTeam' : game[3],
                            'homeScore': game[4]}
                if(game[5]=='EX' or not scorebot.isD1(pwrGameDict['homeTeam'],pwrGameDict['homeTeam'],'Women') or not scorebot.isD1(pwrGameDict['awayTeam'],pwrGameDict['awayTeam'],'Women')):
                    continue
                if(pwrGameDict['homeTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['homeTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0 ,'teamsPlayed': [], "Rating" : 100}})
                if(pwrGameDict['awayTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['awayTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0, 'teamsPlayed': [], "Rating" : 100}})
                
                if(int(pwrGameDict['homeScore']) > int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Wins'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Losses'].append(pwrGameDict['homeTeam'])
                    
                elif(int(pwrGameDict['homeScore']) == int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Ties'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Ties'].append(pwrGameDict['homeTeam'])
                else:
                    teamDict[pwrGameDict['homeTeam']]['Losses'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Wins'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['teamsPlayed'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['teamsPlayed'].append(pwrGameDict['awayTeam'])  
                

    for team in teamDict.keys():
        teamDict[team]['Ratio'] = (len(teamDict[team]["Wins"])+len(teamDict[team]["Ties"])*.5)/(len(teamDict[team]["Losses"])+len(teamDict[team]["Ties"])*.5)

    converged = False
    while(not converged):
        for team in teamDict.keys():
            tWFactor = 0
            sumKrach = 0
            for oppo in set(teamDict[team]['teamsPlayed']):
                sumKrach += (teamDict[team]['Rating']*teamDict[team]['teamsPlayed'].count(oppo))/(teamDict[team]['Rating']+teamDict[oppo]['Rating'])
            newRating = ((len(teamDict[team]['Wins'])+len(teamDict[team]['Ties'])*.5)/sumKrach)*teamDict[team]['Rating']
            ratio = math.fabs(1-(newRating/ teamDict[team]['Rating']))

            if(ratio <= 0.00001):
                converged=True
            teamDict[team]['Rating']= newRating
        if(converged):
            break

    for i in range(10):
        scale_wins = 0
        for team in teamDict.keys():
            scale_wins += 100/(100 + teamDict[team]['Rating'])
        scale = scale_wins/20
        
        for team in teamDict.keys():
            teamDict[team]['Rating'] *= scale
            
    
    team1Odds = teamDict[team1]['Rating']/(teamDict[team1]['Rating']+teamDict[team2]['Rating'])
    team2Odds = teamDict[team2]['Rating']/(teamDict[team1]['Rating']+teamDict[team2]['Rating'])
    
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))  

def getWOdds3(team1,team2):
    
    global teamDict,season
    url = "http://www.collegehockeystats.net/{}/schedules/ncw".format(season)
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"                
        
    team1 = decodeTeam(team1)
    team2 = decodeTeam(team2)
    if(not scorebot.isD1(team1,team1,'Women')):
        return "Team 1 Not Found"
    
    if(not scorebot.isD1(team2,team2,'Women')):
        return "Team 2 Not Found"
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
                elif(game.count('5OT')>0):
                    numOT = '5OT'
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
                game[4] = game[4].replace(' 2OT','')
                game[4] = game[4].replace(' 3OT','')
                game[4] = game[4].replace(' 4OT','')
                game[4] = game[4].replace(' 5OT','')
                pwrGameDict = {'awayTeam' : game[0],
                            'awayScore': game[1],
                            'homeTeam' : game[3],
                            'homeScore': game[4]}
                if(game[5]=='EX' or not scorebot.isD1(pwrGameDict['homeTeam'],pwrGameDict['homeTeam'],'Women') or not scorebot.isD1(pwrGameDict['awayTeam'],pwrGameDict['awayTeam'],'Women')):
                    continue
                if(pwrGameDict['homeTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['homeTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0 ,'teamsPlayed': [], "Rating" : 100}})
                if(pwrGameDict['awayTeam'] not in teamDict):
                    teamDict.update({pwrGameDict['awayTeam']: {"Wins":[], "Losses" : [], "Ties": [], "GP": 0, "WP" : 0, "RRWP": 0, "Ratio": 0, 'SOS' : 0, 'teamsPlayed': [], "Rating" : 100}})
                
                if(int(pwrGameDict['homeScore']) > int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Wins'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Losses'].append(pwrGameDict['homeTeam'])
                    
                elif(int(pwrGameDict['homeScore']) == int(pwrGameDict['awayScore'])):
                    teamDict[pwrGameDict['homeTeam']]['Ties'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Ties'].append(pwrGameDict['homeTeam'])
                else:
                    teamDict[pwrGameDict['homeTeam']]['Losses'].append(pwrGameDict['awayTeam'])
                    teamDict[pwrGameDict['awayTeam']]['Wins'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['GP'] += 1
                teamDict[pwrGameDict['awayTeam']]['teamsPlayed'].append(pwrGameDict['homeTeam'])
                teamDict[pwrGameDict['homeTeam']]['teamsPlayed'].append(pwrGameDict['awayTeam'])  
                

    for team in teamDict.keys():
        teamDict[team]['Ratio'] = (len(teamDict[team]["Wins"])+len(teamDict[team]["Ties"])*.5)/(len(teamDict[team]["Losses"])+len(teamDict[team]["Ties"])*.5)

    converged = False
    while(not converged):
        for team in teamDict.keys():
            tWFactor = 0
            sumKrach = 0
            for oppo in set(teamDict[team]['teamsPlayed']):
                sumKrach += (teamDict[team]['Rating']*teamDict[team]['teamsPlayed'].count(oppo))/(teamDict[team]['Rating']+teamDict[oppo]['Rating'])
            newRating = ((len(teamDict[team]['Wins'])+len(teamDict[team]['Ties'])*.5)/sumKrach)*teamDict[team]['Rating']
            ratio = math.fabs(1-(newRating/ teamDict[team]['Rating']))

            if(ratio <= 0.00001):
                converged=True
            teamDict[team]['Rating']= newRating
        if(converged):
            break

    for i in range(10):
        scale_wins = 0
        for team in teamDict.keys():
            scale_wins += 100/(100 + teamDict[team]['Rating'])
        scale = scale_wins/20
        
        for team in teamDict.keys():
            teamDict[team]['Rating'] *= scale
            
    team1Odds = (teamDict[team1]['Rating']**2 * (teamDict[team1]['Rating'] + 3 * teamDict[team2]['Rating']))/((teamDict[team1]['Rating'] + teamDict[team2]['Rating'])**3)
    team2Odds = (teamDict[team2]['Rating']**2 * (teamDict[team2]['Rating'] + 3 * teamDict[team1]['Rating']))/((teamDict[team2]['Rating'] + teamDict[team1]['Rating'])**3)
        
    return "{} {}%\n{} {}%".format(team1,round(team1Odds*100,1), team2, round(team2Odds*100,1))  
 
def getGTTitle():
    text='No Title Set'
    upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTTitle.txt'
    if(os.path.exists(upGTFilePath)):
        file=open(upGTFilePath,'r')
        text = file.readline()
        text=text.rstrip('\n')
        file.close()
    return "> "+text
    
def setGTTitle(title):
    upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTTitle.txt'
    file2=open(upGTFilePath,'w')
    title = title.replace('"','')
    print(title,end='',file=file2)
    file2.close()
    return "Title Updated: {}".format(title)
    
    
def getGTVid():
    upGTVideoPath = '/home/nmemme/ch_scorebot/titles/upcomingGTvideo.txt'
    currGTVideoPath = '/home/nmemme/ch_scorebot/titles/currentGTvideo.txt'
    text = 'No Video Set'
    if(os.path.exists(upGTVideoPath)):
        file=open(upGTVideoPath,'r')
        text = file.readline()
        text=text.rstrip('\n')
        file.close()
    elif(os.path.exists(currGTVideoPath)):
        file=open(currGTVideoPath,'r')
        text = file.readline()
        text=text.rstrip('\n')
        file.close()
    
    return "> "+text
    
def setGTVid(vid):
    upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTvideo.txt'
    file2=open(upGTFilePath,'w')
    vid = vid.replace('"','')
    print(vid,end='',file=file2)
    file2.close()
    return "New GT Vid: {}".format(vid)
    
def resetGTVid():
    upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTvideo.txt'
    file2=open(upGTFilePath,'w')
    vid="https://www.youtube.com/watch?v=o0YWRXJsMyM"
    vid = vid.replace('"','')
    print(vid,end='',file=file2)
    file2.close()
    return "New GT Vid: {}".format(vid)
    
    
def getTrashTitle():
    text='No Title Set'
    upTTTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingTrashTitle.txt'
    if(os.path.exists(upTTTFilePath)):
        file=open(upTTTFilePath,'r')
        text = file.readline()
        text=text.rstrip('\n')
        text= "> " + text + " EDITION"
        file.close()
    return text
    
def setTrashTitle(title):
    upTTTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingTrashTitle.txt'
    file2=open(upTTTFilePath,'w')
    title = title.replace('"','')
    title = title.upper()
    print(title,end='',file=file2)
    file2.close()
    return "Title Updated: {} EDITION".format(title)

@client.event
async def on_message(message):
    global invalidRoles
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!help') or message.content.startswith('?help'):
       helpStr = displayHelp()
       await message.author.send(helpStr[0])
       await message.author.send(helpStr[1])
    if not message.content.startswith('?'):
        return
                
    loop = asyncio.get_event_loop()
    
    if message.content.startswith('?getgttitle') and message.author.name == 'memmdog':
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getGTTitle)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?setgttitle ') and message.author.name == 'memmdog':
        title = message.content.split('?setgttitle ')[1]
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, setGTTitle,title)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?getgtvid') and message.author.name == 'memmdog':
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getGTVid)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?setgtvid ') and message.author.name == 'memmdog':
        vid = message.content.split('?setgtvid ')[1]
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, setGTVid,vid)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?resetgtvid') and message.author.name == 'memmdog':
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, resetGTVid)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?gettrashtitle') and message.author.name == 'memmdog':
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getTrashTitle)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?settrashtitle ') and message.author.name == 'memmdog':
        title = message.content.split('?settrashtitle ')[1]
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, setTrashTitle,title)
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
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
        team = message.content.split('?msched ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?sched '):
        team = message.content.split('?sched ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wsched '):
        team = message.content.split('?wsched ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getSchedule, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
          
    if message.content.startswith('?mres '):
        team = message.content.split('?mres ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?res '):
        team = message.content.split('?res ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wres '):
        team = message.content.split('?wres ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg) 

    if message.content.startswith('?mform '):
        team = message.content.split('?mform ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?form '):
        team = message.content.split('?form ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
    
    if message.content.startswith('?wform '):
        team = message.content.split('?wform ')[1]
        split=team.split(',')
        if(len(split)==2):
            opt=split[1]
            opt=opt.lstrip(' ')
            team=split[0]
        else:
            opt = '5'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getResults, team, opt,"Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)              
      
    if message.content.startswith('?mstats '):
        team = message.content.split('?mstats ')[1]
        split=team.split(',')
        if(len(split)==2):
            player=split[1]
            player=player.lstrip(' ')
            team=split[0]
        else:
            player='N/A'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getStats, team, player, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)

    if message.content.startswith('?stats '):
        team = message.content.split('?stats ')[1]
        split=team.split(',')
        if(len(split)==2):
            player=split[1]
            player=player.lstrip(' ')
            team=split[0]
        else:
            player='N/A'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getStats, team, player, "Men")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
            
    if message.content.startswith('?wstats '):
        team = message.content.split('?wstats ')[1]
        split=team.split(',')
        if(len(split)==2):
            player=split[1]
            player=player.lstrip(' ')
            team=split[0]
        else:
            player='N/A'
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getStats, team, player, "Women")
            p.shutdown()
        if(len(msg)>0):
            await message.channel.send(msg)
            
    if message.content.startswith('?thanksbot'):
        msg = "You're Welcome {0.author.mention}!".format(message)
        for i in range(len(message.author.roles)):
            if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch" and message.author.roles[-1-i].name !=  "Craig"):
                cheer = getCheer(message.author.roles[-1-i].name)
                break
      
        if(cheer!=""):
            msg+="\n{}".format(cheer)
        await message.channel.send(msg)

    
    if message.content.startswith('?cheer'):
        teamChoice = message.content.split('?cheer ')
        if(len(teamChoice)>1):
            team=decodeTeam(teamChoice[1])
        if(len(teamChoice)==1):
            for i in range(len(message.author.roles)):
                if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch" and message.author.roles[-1-i].name !=  "Craig"):
                    cheer = getCheer(message.author.roles[-1-i].name)
                    break
        else:
            cheer = getCheer(convertTeamtoDisRole(team))
            
        if(cheer!=""):
            msg="{}".format(cheer)
        else:
            #msg = "I don't know that cheer."
            teamName=team
            if(convertTeamtoDisRole(team) != ""):
                teamName = convertTeamtoDisRole(team)
            msg = "Go {}!".format(teamName)
        await message.channel.send(msg)
        
    if message.content.startswith('?jeer '):
        teamChoice = message.content.split('?jeer ')
        jeer = ""
        if(len(teamChoice)>1):
            team=decodeTeam(teamChoice[1])
            jeer = getJeer(convertTeamtoDisRole(team))
            
        if(jeer!=""):
            msg="{}".format(jeer)
        else:
            #msg = "I don't know that jeer."
            teamName=team
            if(convertTeamtoDisRole(team) != ""):
                teamName = convertTeamtoDisRole(team)
            msg = "Boo {}".format(teamName)
        await message.channel.send(msg)
    if message.content.startswith('?boo '):
        teamChoice = message.content.split('?boo ')
        jeer = ""
        if(len(teamChoice)>1):
            team = decodeTeam(teamChoice[1])
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
                
    if(message.content.startswith('?mpwr')):
        opt = message.content.split('?mpwr ')
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
                
    if(message.content.startswith('?wkrach')):
        opt = message.content.split('?wkrach ')
        if(len(opt)==1):
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWKRACH, '')
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWKRACH, opt[1])
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg) 
                 
                
    if(message.content.startswith('?stand')):
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
            conf = message.content.split('?stand ')
            if(len(conf)>1):
                with cf.ProcessPoolExecutor(1) as p:
                    msg = await loop.run_in_executor(p, getStandings, conf[1], "Men")
                    p.shutdown()
                if(len(msg)>0):
                    await message.channel.send(msg)
            else:
                    await message.channel.send("I don't know that conference.")    
    
    if(message.content.startswith('?mstand')):
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
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
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
            conf = message.content.split('?wstand ')
            if(len(conf)>1):
                with cf.ProcessPoolExecutor(1) as p:
                    msg = await loop.run_in_executor(p, getStandings, conf[1], "Women")
                    p.shutdown()
                if(len(msg)>0):
                    await message.channel.send(msg)
            else:
                    await message.channel.send("I don't know that conference.")
                    
    '''                
    if(message.content.startswith('?mhepi')):
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getHEPI, "men")
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
           
    if(message.content.startswith('?hepi')):
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getHEPI, "men")
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
 
    if(message.content.startswith('?whepi')):
        if(message.channel.name == 'game-night'):
            await message.channel.send("Please use #bot-dump")
        else:
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getHEPI, "women")
                p.shutdown()
            if(len(msg)>0):
                await message.channel.send(msg)
    '''            
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
             
    if(message.content.startswith('?history ')):
        team1= ''
        team2= ''
        teams = message.content.split('?history ')
        
        if(len(teams)>1): 
            if(teams[1].count(',')==1):
                team1,team2 = teams[1].split(",")
                team1=team1.rstrip(" ")
                team2=team2.lstrip(' ')
                numGames='5'
                with cf.ProcessPoolExecutor(1) as p:
                    msg = await loop.run_in_executor(p, getMatchupHistory,  team1, team2,numGames)
                    p.shutdown()
                if(len(msg)>0):
                    await message.channel.send(msg)
                
            elif(teams[1].count(',')==2):
                team1,team2,numGames = teams[1].split(",")
                team1=team1.rstrip(" ")
                team2=team2.lstrip(' ')

                with cf.ProcessPoolExecutor(1) as p:
                    msg = await loop.run_in_executor(p, getMatchupHistory,  team1, team2,numGames)
                    p.shutdown()
                if(len(msg)>0):
                    await message.channel.send(msg)
            else:
             await message.channel.send("Invalid number of teams, enter two comma separated teams")
        else:
             await message.channel.send("Invalid number of teams, enter two comma separated teams")
             
    if(message.content.startswith('?wodds ')):
        team1= ''
        team2= ''
        teams = message.content.split('?wodds ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
                
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWOdds,  team1, team2)
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
             
    if(message.content.startswith('?wodds3 ')):
        team1= ''
        team2= ''
        teams = message.content.split('?wodds3 ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
                
            with cf.ProcessPoolExecutor(1) as p:
                msg = await loop.run_in_executor(p, getWOdds3,  team1, team2)
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
                if(roles != "```\n"):
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
    
    if(message.content.startswith('?pdoplot') or message.content.startswith('?pdo')):
        gender='Mens'        
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generatePDOPlot, gender)
            p.shutdown()
        await message.channel.send(file=discord.File(msg))
        
    if(message.content.startswith('?pdwoplot') or message.content.startswith('?pdwo') or message.content.startswith('?wpdo') or message.content.startswith('?wpdoplot')):
        gender='Womens'        
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generatePDOPlot, gender)
            p.shutdown()
        await message.channel.send(file=discord.File(msg))
        
    if(message.content.startswith('?corsiplot') or message.content.startswith('?corsi')):
        gender='Mens'        
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generateCorsiPlot, gender)
            p.shutdown()
        await message.channel.send(file=discord.File(msg))
    
    if(message.content.startswith('?chain')):
        team1= ''
        team2= ''
        teams = message.content.split('?chain ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
            
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getTransitiveWinChain, team1,team2)
            p.shutdown()
        await message.channel.send(msg)
        
    if(message.content.startswith('?whosbetter')):
        team1= ''
        team2= ''
        teams = message.content.split('?whosbetter ')

        if(len(teams)>1 and teams[1].count(',')==1): 
            team1,team2 = teams[1].split(",")
            team1=team1.rstrip(" ")
            team2=team2.lstrip(' ')
            
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, getTransitiveWinChain, team1,team2)
            p.shutdown()
        await message.channel.send(msg)                   
                
    if(message.content.startswith('?wcorsiplot') or message.content.startswith('?wcorsi')):
        gender='Womens'        
        with cf.ProcessPoolExecutor(1) as p:
            msg = await loop.run_in_executor(p, generateCorsiPlot, gender)
            p.shutdown()
        await message.channel.send(file=discord.File(msg))
        
    if(message.content.startswith('?scoreboard')):
            await message.channel.send("http://www.collegehockeyinc.com/nationalscores.php")
     
    # gifs and stuff
    if(message.content.startswith('?bu')):
            await message.channel.send("https://media.giphy.com/media/mACM98U3XELWlpDxEO/giphy.mp4")
            
    if(message.content.startswith('?goodgoal')):
            await message.channel.send("https://gfycat.com/lastingcomplexblackbuck")
            
    if(message.content.startswith('?nogoal')):
            await message.channel.send("https://media.giphy.com/media/q01IxfTXuoP4Y/giphy.mp4")  

    if(message.content.startswith('?savory')):
            await message.channel.send("https://media.giphy.com/media/ozTKmmDCcE9pMNWMXF/giphy.mp4")
            
    if(message.content.startswith('?uml')):
            await message.channel.send("https://media.giphy.com/media/ejDkNiozRxVwUtbbpN/giphy.mp4")
    
    if(message.content.startswith('?lowellbu')):
            await message.channel.send("https://media.giphy.com/media/J5jccTVhlkKhogi6DP/giphy.mp4")
            
    if(message.content.startswith('?harvard')):
            await message.channel.send("FUCK HARVARD")
        
    if(message.content.startswith('?boston') and not message.content.startswith('?bostoncollege')):
            gif="https://m.imgur.com/ZPZUGW0"
#            random.seed(datetime.datetime.now())
#            if(random.randint(0,100)<=10):
#                gif="https://media.giphy.com/media/W2zqB99rxiTxDNT1Ci/giphy.gif"
            
            await message.channel.send(gif)
            
    if(message.content.startswith('?nuboston')):
            await message.channel.send("https://media.giphy.com/media/WU0oTNSciD83BUDfYR/giphy.gif")
            
    if(message.content.startswith('?redjd')):
            await message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/680861939047333971/3pzph6.png")
    
    if(message.content.startswith('?lowell') and not message.content.startswith('?lowellbu')):
            await message.channel.send("https://imgur.com/a/C9aSorC")
            
    if(message.content.startswith('?northdakota')):
            await message.channel.send("F'IN HAWKS")
            
    if(message.content.startswith('?jerry')):
            await message.channel.send("https://imgur.com/a/mejC6E2")
            #await message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/691772255306514552/hyW6VMD.png")
    
    if(message.content.startswith('?bcot')):
            await message.channel.send('"free" "hockey" in "Boston"')  

    if(message.content.startswith('?oti')):
            await message.channel.send('**ON THE ICE**')             

    if(message.content.startswith('?bc') and not message.content.startswith('?bcot')):
            await message.channel.send("https://media.giphy.com/media/E327kKMf0RKHAB1jpu/giphy.gif")

    if(message.content.startswith('?uconn')):
            await message.channel.send("https://imgur.com/a/gWy8Ifj")
            
    if(message.content.startswith('?unh')):
            await message.channel.send("https://imgur.com/a/mq8brow")
            
    if(message.content.startswith('?mankato')):
    #        await message.channel.send("https://i.imgur.com/2B2iSkt.jpg")
            await message.channel.send(" https://media.giphy.com/media/66nOBbUf0MqbOU4DYR/giphy.gif")
   
            
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
            await message.channel.send("https://www.youtube.com/watch?v=0bGpREk4Cw4")
            
    if(message.content.startswith('?dartmouth')):
            await message.channel.send("https://www.youtube.com/watch?v=Qe3iNZjenvI")
            
    if(message.content.startswith('?pennstate')):
            await message.channel.send("https://imgur.com/a/uhqlM9S")
            
    if(message.content.startswith('?rpi')):
            await message.channel.send("https://imgur.com/uAndWDQ")
            
    if(message.content.startswith('?umass') and not message.content.startswith('?umassamherst')):
            await message.channel.send("When they beat Providence tonight it will be legitimate proof that UMass deserves all of the recognition that it has received. They are 6-1 on the season and 3-0 in the conference which is an extremely impressive feat considering 2 years ago the team was not even ranked nationally.")
            
    if(message.content.startswith('?umassamherst')):
            await message.channel.send('https://cdn.discordapp.com/attachments/523161681484972062/909470794625712158/unknown.png')  
    
    if(message.content.startswith('?amherst')):
            await message.channel.send("If you are being recruited and want to play in a program that wins championships, develops you on and off the ice, invests in your long-term success and prepares you for pro hockey, there’s no better place than @UMassHockey. Believe it.")  
    if(message.content.startswith('?cornell')):
            await message.channel.send("I think you should mentally and emotionally prepare yourself that at some point Cornell University will raise two national championship banners for this lost season.\nThe students and alumni base is not going to give a shit about counter-arguments (you're welcome to declare yourselves pairwise champions) and are not going to just shrug off both the best Mens and Womens teams in several decades as a lost cause. It's going to happen, and in a few decades no one will even think it particularly controversial.")
    
    if(message.content.startswith('?maine')):
            await message.channel.send("https://i.imgur.com/4ZTkTXX.gifv")
            
    if(message.content.startswith('?newhampshire')):
            await message.channel.send("https://i.imgur.com/jWX20zw.gifv")
   
    if(message.content.startswith('?connecticut')):
            await message.channel.send("https://imgur.com/a/cJLxgm2")
        
    if(message.content.startswith('?eng') or message.content.startswith('?emptynet')):
            await message.channel.send("https://imgur.com/a/y8w9Y1X")
            
    if(message.content.startswith('?bread')):
            await message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/685911017334767840/unknown.png")        
              
    if(message.content.startswith('?bgsu') or message.content.startswith('?bowlinggreen')):
            await message.channel.send("https://media.giphy.com/media/Nv391J41hh34oL34Xr/giphy.gif")
     
    if(message.content.startswith('?hocro') or message.content.startswith('?holycross') or message.content.startswith('?hc')):
            await message.channel.send("https://media.giphy.com/media/yg3AWJeOza2XGpXRt7/giphy.gif")     
            
    if(message.content.startswith('?bemidji')):
            await message.channel.send("https://www.youtube.com/watch?v=CW_B4KB0wYs")
            
    if(message.content.startswith('?nodak')):
            await message.channel.send("https://www.youtube.com/watch?v=-B2vE1Yl2_c")
            
    if(message.content.startswith('?mtu')):
            await message.channel.send("https://www.youtube.com/watch?v=FZQ6VNWvmOc")
    
    if(message.content.startswith('?northeastern') and not message.content.startswith('?northeasternwins')):
            await message.channel.send("https://media.giphy.com/media/jt8C9VdM1Xo6SY2Yib/giphy.gif")
            
    if(message.content.startswith('?wnortheastern')):
            await message.channel.send("https://media.giphy.com/media/008VqVNcINvZbQq7oH/giphy.mp4")       
            
    if(message.content.startswith('?rit')):
            await message.channel.send("https://j.gifs.com/q75jR0.gif")
            
    if(message.content.startswith('?almostchaos')):
            await message.channel.send("https://media.giphy.com/media/26ybwvTX4DTkwst6U/giphy.gif")

    if(message.content.startswith('?russia')):
            await message.channel.send("https://media.giphy.com/media/W3keAf3qh6MwXZ8ddc/giphy.mp4")
            
    if(message.content.startswith('?wisconsin')):
            await message.channel.send("https://media.giphy.com/media/Ox6839VK0vCPTakv8H/giphy.gif")
            
    if(message.content.startswith('?colgate') or message.content.startswith('?gate')):
            await message.channel.send("https://gfycat.com/agitatedslimyhyrax")        
        
    if(message.content.startswith('?portal')):
            await message.channel.send(random.choice([ "https://tenor.com/view/chosen-toy-story-gif-7936264","https://media.giphy.com/media/ciadMxfm3135m/giphy.gif"]))      
                
    if(message.content.startswith('?dog') or message.content.startswith('?doggo') or message.content.startswith('?doggy')):
            opt = message.content.split(' ')
            if(len(opt)>1):
                await message.channel.send(getDog(opt[1]))
            else:
                await message.channel.send(getDog(opt[0]))
    if(message.content.startswith('?cat') or message.content.startswith('?kitty')):         
        await message.channel.send(getCat())
        
    if(message.content.startswith('?hearef') or message.content.startswith('?heref')): 
        #for i in message.guild.emojis:
        #   print("<:{}:{}>".format(i.name, i.id))
        await message.channel.send('EXPERIENCE HOCKEY EAST OFFICIATING')
    
    if(message.content.startswith('?beanpot') and not message.content.startswith('?beanpottrot')):
        await message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/651597256553660416/geeboston.jpg")
        
    if(message.content.startswith('?beanpottrot')):
        await message.channel.send("https://www.youtube.com/watch?v=EC2cs88XK1g")
        
    if(message.content.startswith('?beanpawt')):
        await message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/761742817025327114/IMG_20201002_201354.jpg")
        
    if(message.content.startswith('?bostoncollege') or message.content.startswith('?chestnuthilluniversity') or message.content.startswith('?chestnuthillcommunitycollege')):
        await message.channel.send("https://media.giphy.com/media/cnEz7n3MhAIbESshGd/giphy.gif")
   
    if(message.content.startswith('?puckman')):
        await message.channel.send("https://media.discordapp.net/attachments/519719563294801922/716448834703589397/mascotmadness.png")
        
    if(message.content.startswith('?playoffot') or message.content.startswith('?playoffOT') ):
        await message.channel.send("https://twitter.com/jon_bois/status/456616952153128960")    
   
    if(message.content.startswith('?merrimack') or message.content.startswith('?mack') ):
        await message.channel.send("Is Merrimack College a respectable institution?")   

    if(message.content.startswith('?btn+')):
        await message.channel.send("There are no non-paid streams for BTN+ games available, might I suggest locating the team's radio broadcast")  
    
    if(message.content.startswith('?huskyalliance')):
        await message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/821574872290295849/image0.jpg")  
        
    if(message.content.startswith('?post')):
        await message.channel.send("PING!")
        
    if(message.content.startswith('?flagship')):
        await message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/821215322823458826/image0.jpg")  
    
    if(message.content.startswith('?five-0') or message.content.startswith('?five-o')):
        await message.channel.send("https://www.youtube.com/watch?v=MC64gKvh5R8") 
        
    if(message.content.startswith('?stferrous')):
        await message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/829934423310204948/StFerrous.png")
    
    if(message.content.startswith('?redsoxwin') or message.content.startswith('?dirtywater')):
        await message.channel.send("https://youtu.be/5apEctKwiD8")
    
    if(message.content.startswith('?metcalf')):
        await message.channel.send("Win your games and don’t worry about this!!")
    
    if(message.content.startswith('?botscores') or message.content.startswith('?botscore')):
        await message.channel.send("Anyone: hey Dr Bot i want a score\nBot: Sure thing! Here you go buddy!!\nAnyone: This score is wrong! You Suck!\nBot: :sob::sob::sob:")
        
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
        "gate" : "Colgate",
        "chestnuthillcommunitycollege" : "Boston College",
        "chestnuthilluniversity" : "Boston College",
        "clarky" : "Clarkson",
        "cct" : "Clarkson",
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
        "nodak" : "North Dakota",
        "nu" : "Northeastern",
        "osu" : "Ohio State",
        "pc" : "Providence",
        "pianohuskies" : "Michigan Tech",
        "prinny" : "Princeton",
        "psu" : "Penn State",
        "purplecows" : "Minnesota State",
        "qu" : "Quinnipiac",
        "quinny" : "Quinnipiac",
        "quinni" : "Quinnipiac",
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
        "stthomas" : "St. Thomas",
        "ust" : "St. Thomas",
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
        "uma" : "Massachusetts",
        "umassamherst" : "Massachusetts",
        "umasslowell" : "UMass Lowell",
        "umd" : "Minnesota Duluth",
        "uml" : "UMass Lowell",
        "umo" : "Maine",
        "umaine" : "Maine",
        "umtc" : "Minnesota",
        "umn" : "Minnesota",
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
        "voter" : "Voter",
        "poll" : "Voter",
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
    teamDict = {"Air Force" : "team/Air-Force/1/",
        "Alaska":"team/Alaska/4",
        "American Int'l" : "team/American-Intl/5/",
        "Arizona State" : "team/Arizona-State/61/",
        "Army" : "team/Army/6/",
        "Bemidji State" : "team/Bemidji-State/7/",
        "Bentley" : "team/Bentley/8/",
        "Boston College" : "team/Boston-College/9/",
        "Boston University" : "team/Boston-University/10/",
        "Bowling Green" : "team/Bowling-Green/11/",
        "Brown" : "team/Brown/12/",
        "Canisius" : "team/Canisius/13/",
        "Clarkson" : "team/Clarkson/14/",
        "Colgate" : "team/Colgate/15/",
        "Colorado College" : "team/Colorado-College/16/",
        "Connecticut" : "team/Connecticut/17/",
        "Cornell" : "team/Cornell/18/",
        "Dartmouth" : "team/Dartmouth/19/",
        "Denver" : "team/Denver/20/",
        "Ferris State" : "team/Ferris-State/21/",
        "Franklin Pierce" : "team/Franklin-Pierce/406/",
        "Harvard" : "team/Harvard/22/",
        "Holy Cross" : "team/Holy-Cross/23/",
        "Lake Superior" : "team/Lake-Superior/24/",
        "Lindenwood" : "team/Lindenwood/433/",
        "Long Island" : "team/Long-Island/62/",
        "Maine" : "team/Maine/25/",
        "Mass.-Lowell" : "team/Mass-Lowell/26/",
        "Massachusetts" : "team/Massachusetts/27/",
        "Mercyhurst" : "team/Mercyhurst/28/",
        "Merrimack" : "team/Merrimack/29/",
        "Miami" : "team/Miami/30/",
        "Michigan State" : "team/Michigan-State/32/",
        "Michigan Tech" : "team/Michigan-Tech/33/",
        "Michigan" : "team/Michigan/31/",
        "Minnesota State" : "team/Minnesota-State/35/",
        "Minnesota" : "team/Minnesota/34/",
        "Minnesota-Duluth" : "team/Minnesota-Duluth/36/",
        "New Hampshire" : "team/New-Hampshire/38/",
        "Niagara" : "team/Niagara/39/",
        "North Dakota" : "team/North-Dakota/40/",
        "Northeastern" : "team/Northeastern/41/",
        "Northern Michigan" : "team/Northern-Michigan/42/",
        "Notre Dame" : "team/Notre-Dame/43/",
        "Ohio State" : "team/Ohio-State/44/",
        "Omaha" : "team/Omaha/37/",
        "Penn State" : "team/Penn-State/60/",
        "Post" : "team/Post/434/",
        "Princeton" : "team/Princeton/45/",
        "Providence" : "team/Providence/46/",
        "Quinnipiac" : "team/Quinnipiac/47/",
        "RIT" : "team/RIT/49/",
        "Rensselaer" : "team/Rensselaer/48/",
        "Robert Morris" : "team/Robert-Morris/50/",
        "Sacred Heart" : "team/Sacred-Heart/51/",
        "Saint Anselm" : "team/Saint-Anselm/419/",
        "Saint Michael's" : "team/Saint-Michaels/421/",
        "St. Cloud State" : "team/St-Cloud-State/52/",
        "St. Lawrence" : "team/St-Lawrence/53/",
        "St. Thomas" : "team/St-Thomas/63/",
        "Syracuse" : "team/Syracuse/423/",
        "Union" : "team/Union/54/",
        "Vermont" : "team/Vermont/55/",
        "Western Michigan" : "team/Western-Michigan/57/",
        "Wisconsin" : "team/Wisconsin/58/",
        "Yale" : "team/Yale/59/"}


    decTeam = decodeTeam(team)
    decTeam2 = '' 
    if(decTeam in chnDiffs.keys()):
        decTeam=chnDiffs[decTeam]
    if(scorebot.isD1(decTeam,decTeam,gender) or decTeam in chnDiffs.values()):
       if(gender=="Men"):
          sched='schedules'
       elif(gender=="Women"):
          sched='women'
       url = "https://www.collegehockeynews.com/{}/{}".format(sched,teamDict[decTeam])
    else:
        return ":regional_indicator_x: Team Not Found"
        
    if(opt.isnumeric()):
        numGames = int(opt)
    else:
        decTeam2 = decodeTeam(opt)
        if(decTeam2 in chnDiffs.keys()):
            decTeam2 = chnDiffs[decTeam2]
        numGames=10
            
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
           

    schedule = soup.find('table',{'class':'data schedule'})
    gameList=schedule.find_all('tr')
    games = []
    for i in gameList:
        col=i.find_all('td')
        if(len(col)==1):
            month=col[0].get_text().split(' ')[0]
            continue
        counter=0
        col=col[0].get_text().rstrip('\n\n')
        col=col.replace('\xa0',' ')
        colData=col.split('\n')
        date=(month[:3]+' '+colData[0]).split('\t')[0]
        date=date.split(' ')
        date="{}, {} {}".format(date[2],date[0],date[1])
        result=colData[1].split('\t')
        time=colData[-1].rstrip(' ')
        loc=colData[3]
        opp=colData[4]
        ot=''
        if(colData[2]!=''):
            ot='('+colData[2].upper()+')'
        if(loc==''):
            opp=opp.upper()
        if(len(result)>2):
            score=result[1]+' '+result[2]
            result=result[0] + ' ' + ot
            if(decTeam2.lower()==opp.lower().replace(" (nc)",'')):
                games.append("{} {} {} {}\n".format(date,opp,score,result))
        elif(decTeam2!='' and decTeam2.lower()==opp.lower().replace(" (nc)",'')):
            games.append("{} {} {}\n".format(date,opp,time))
        elif(decTeam2==''):
            games.append("{} {} {}\n".format(date,opp,time))
            
    gameLine = '```\n'
    counter=0
    for i in games:
        gameLine += i
        counter+=1
        if(counter>=numGames):
            break
    gameLine +='```'
    if(gameLine=='```\n```'):
        return 'No Schedule Found'
    
    return gameLine
    
def getResults(team,opt,gender):
    global chnDiffs
    teamDict = {"Air Force" : "team/Air-Force/1/",
        "Alaska":"team/Alaska/4",
        "American Int'l" : "team/American-Intl/5/",
        "Arizona State" : "team/Arizona-State/61/",
        "Army" : "team/Army/6/",
        "Bemidji State" : "team/Bemidji-State/7/",
        "Bentley" : "team/Bentley/8/",
        "Boston College" : "team/Boston-College/9/",
        "Boston University" : "team/Boston-University/10/",
        "Bowling Green" : "team/Bowling-Green/11/",
        "Brown" : "team/Brown/12/",
        "Canisius" : "team/Canisius/13/",
        "Clarkson" : "team/Clarkson/14/",
        "Colgate" : "team/Colgate/15/",
        "Colorado College" : "team/Colorado-College/16/",
        "Connecticut" : "team/Connecticut/17/",
        "Cornell" : "team/Cornell/18/",
        "Dartmouth" : "team/Dartmouth/19/",
        "Denver" : "team/Denver/20/",
        "Ferris State" : "team/Ferris-State/21/",
        "Franklin Pierce" : "team/Franklin-Pierce/406/",
        "Harvard" : "team/Harvard/22/",
        "Holy Cross" : "team/Holy-Cross/23/",
        "Lake Superior" : "team/Lake-Superior/24/",
        "Lindenwood" : "team/Lindenwood/433/",
        "Long Island" : "team/Long-Island/62/",
        "Maine" : "team/Maine/25/",
        "Mass.-Lowell" : "team/Mass-Lowell/26/",
        "Massachusetts" : "team/Massachusetts/27/",
        "Mercyhurst" : "team/Mercyhurst/28/",
        "Merrimack" : "team/Merrimack/29/",
        "Miami" : "team/Miami/30/",
        "Michigan State" : "team/Michigan-State/32/",
        "Michigan Tech" : "team/Michigan-Tech/33/",
        "Michigan" : "team/Michigan/31/",
        "Minnesota State" : "team/Minnesota-State/35/",
        "Minnesota" : "team/Minnesota/34/",
        "Minnesota-Duluth" : "team/Minnesota-Duluth/36/",
        "New Hampshire" : "team/New-Hampshire/38/",
        "Niagara" : "team/Niagara/39/",
        "North Dakota" : "team/North-Dakota/40/",
        "Northeastern" : "team/Northeastern/41/",
        "Northern Michigan" : "team/Northern-Michigan/42/",
        "Notre Dame" : "team/Notre-Dame/43/",
        "Ohio State" : "team/Ohio-State/44/",
        "Omaha" : "team/Omaha/37/",
        "Penn State" : "team/Penn-State/60/",
        "Post" : "team/Post/434/",
        "Princeton" : "team/Princeton/45/",
        "Providence" : "team/Providence/46/",
        "Quinnipiac" : "team/Quinnipiac/47/",
        "RIT" : "team/RIT/49/",
        "Rensselaer" : "team/Rensselaer/48/",
        "Robert Morris" : "team/Robert-Morris/50/",
        "Sacred Heart" : "team/Sacred-Heart/51/",
        "Saint Anselm" : "team/Saint-Anselm/419/",
        "Saint Michael's" : "team/Saint-Michaels/421/",
        "St. Cloud State" : "team/St-Cloud-State/52/",
        "St. Lawrence" : "team/St-Lawrence/53/",
        "St. Thomas" : "team/St-Thomas/63/",
        "Syracuse" : "team/Syracuse/423/",
        "Union" : "team/Union/54/",
        "Vermont" : "team/Vermont/55/",
        "Western Michigan" : "team/Western-Michigan/57/",
        "Wisconsin" : "team/Wisconsin/58/",
        "Yale" : "team/Yale/59/"}
      
    team=decodeTeam(team)  
    if(team in chnDiffs.keys()):
        team=chnDiffs[team]
    if(scorebot.isD1(team,team,gender) or team in chnDiffs.values()):
       if(gender=="Men"):
          sched='schedules'
       elif(gender=="Women"):
          sched='women'
       url = "https://www.collegehockeynews.com/{}/{}".format(sched,teamDict[team])
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
    
    schedule = soup.find('table',{'class':'data schedule'})
    gameList=schedule.find_all('tr')
    gameLine = '```\n'
    games = []
    for i in gameList:
        col=i.find_all('td')
        if(len(col)==1):
            month=col[0].get_text().split(' ')[0]
            continue
        counter=0
        col=col[0].get_text().rstrip('\n\n')
        col=col.replace('\xa0',' ')
        colData=col.split('\n')
        date=(month[:3]+' '+colData[0]).split('\t')[0]
        date=date.split(' ')
        date="{}, {} {}".format(date[2],date[0],date[1])
        result=colData[1].split('\t')
        time=colData[-1].rstrip(' ')
        loc=colData[3]
        opp=colData[4]
        ot=''
        if(colData[2]!=''):
            ot='('+colData[2].upper()+')'
        if(loc==''):
            opp=opp.upper()
        if(len(result)>2):
            score=result[1]+' '+result[2]
            result=result[0] + ' ' + ot
            games.append("{} {} {} {}\n".format(date,opp,score,result))
            
    numGames *= -1
    gamesToReport = games[numGames:]
    for i in gamesToReport:
        gameLine+= i
            
    gameLine +='```'
    if(gameLine=='```\n```'):
        return 'No Results Found'
    return gameLine
    
def getStats(team,playerToFind,gender):

    global chnDiffs
    teamDict = {"Air Force" : "team/Air-Force/1/",
        "Alaska":"team/Alaska/4",
        "American Int'l" : "team/American-Intl/5/",
        "Arizona State" : "team/Arizona-State/61/",
        "Army" : "team/Army/6/",
        "Bemidji State" : "team/Bemidji-State/7/",
        "Bentley" : "team/Bentley/8/",
        "Boston College" : "team/Boston-College/9/",
        "Boston University" : "team/Boston-University/10/",
        "Bowling Green" : "team/Bowling-Green/11/",
        "Brown" : "team/Brown/12/",
        "Canisius" : "team/Canisius/13/",
        "Clarkson" : "team/Clarkson/14/",
        "Colgate" : "team/Colgate/15/",
        "Colorado College" : "team/Colorado-College/16/",
        "Connecticut" : "team/Connecticut/17/",
        "Cornell" : "team/Cornell/18/",
        "Dartmouth" : "team/Dartmouth/19/",
        "Denver" : "team/Denver/20/",
        "Ferris State" : "team/Ferris-State/21/",
        "Franklin Pierce" : "team/Franklin-Pierce/406/",
        "Harvard" : "team/Harvard/22/",
        "Holy Cross" : "team/Holy-Cross/23/",
        "Lake Superior" : "team/Lake-Superior/24/",
        "Lindenwood" : "team/Lindenwood/433/",
        "Long Island" : "team/Long-Island/62/",
        "Maine" : "team/Maine/25/",
        "Mass.-Lowell" : "team/Mass-Lowell/26/",
        "Massachusetts" : "team/Massachusetts/27/",
        "Mercyhurst" : "team/Mercyhurst/28/",
        "Merrimack" : "team/Merrimack/29/",
        "Miami" : "team/Miami/30/",
        "Michigan State" : "team/Michigan-State/32/",
        "Michigan Tech" : "team/Michigan-Tech/33/",
        "Michigan" : "team/Michigan/31/",
        "Minnesota State" : "team/Minnesota-State/35/",
        "Minnesota" : "team/Minnesota/34/",
        "Minnesota-Duluth" : "team/Minnesota-Duluth/36/",
        "New Hampshire" : "team/New-Hampshire/38/",
        "Niagara" : "team/Niagara/39/",
        "North Dakota" : "team/North-Dakota/40/",
        "Northeastern" : "team/Northeastern/41/",
        "Northern Michigan" : "team/Northern-Michigan/42/",
        "Notre Dame" : "team/Notre-Dame/43/",
        "Ohio State" : "team/Ohio-State/44/",
        "Omaha" : "team/Omaha/37/",
        "Penn State" : "team/Penn-State/60/",
        "Post" : "team/Post/434/",
        "Princeton" : "team/Princeton/45/",
        "Providence" : "team/Providence/46/",
        "Quinnipiac" : "team/Quinnipiac/47/",
        "RIT" : "team/RIT/49/",
        "Rensselaer" : "team/Rensselaer/48/",
        "Robert Morris" : "team/Robert-Morris/50/",
        "Sacred Heart" : "team/Sacred-Heart/51/",
        "Saint Anselm" : "team/Saint-Anselm/419/",
        "Saint Michael's" : "team/Saint-Michaels/421/",
        "St. Cloud State" : "team/St-Cloud-State/52/",
        "St. Lawrence" : "team/St-Lawrence/53/",
        "St. Thomas" : "team/St-Thomas/63/",
        "Syracuse" : "team/Syracuse/423/",
        "Union" : "team/Union/54/",
        "Vermont" : "team/Vermont/55/",
        "Western Michigan" : "team/Western-Michigan/57/",
        "Wisconsin" : "team/Wisconsin/58/",
        "Yale" : "team/Yale/59/"}
      
    team=decodeTeam(team)  
    if(team in chnDiffs.keys()):
        team=chnDiffs[team]
    if(scorebot.isD1(team,team,gender) or team in chnDiffs.values()):
       if(gender=="Men"):
          stats='stats'
       elif(gender=="Women"):
          stats='women/stats'
       url = "https://www.collegehockeynews.com/{}/{}".format(stats,teamDict[team])
    else:
        return ":regional_indicator_x: Team Not Found"
        
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    skateTable = soup.find('table',{'id':'skaters'})
    gTable = soup.find('table',{'id':'goalies'})
    skbod=skateTable.find('tbody')
    skrows=skbod.find_all('tr')
    gbod=gTable.find('tbody')
    grows=gbod.find_all('tr')
    goalieHeader='Name\t\tYr\tGP\tMin\tGA\tSV%\tGAA\tRecord\tSO\n'
    goalieDict={}
    for goalie in grows:
        col=goalie.find_all('td')
        name,yr=col[0].get_text().lstrip('\n').rstrip('\t\t').split(', ')
        gp=col[1].get_text()
        record="{}-{}-{}".format(col[2].get_text(),col[3].get_text(),col[4].get_text())
        ga=col[5].get_text()
        mins=col[6].get_text()
        gaa=col[7].get_text()
        so=col[8].get_text()
        sv=col[10].get_text()
        goalieDict[name]="{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(name,yr,gp,mins,ga,sv,gaa,record,so)

    skaterHeader='Name\t\tPos\tYr\tGP\tG\tA\tPts\tPIM\t+/-\n'
    skaterDict={}
    for skater in skrows:
        col=skater.find_all('td')
        name,pos,yr=col[0].get_text().lstrip('\n').rstrip('\t\t').split(', ')
        gp=col[1].get_text()
        g=col[2].get_text()
        a=col[3].get_text()
        pts=col[4].get_text()
        pim=col[8].get_text()
        p_m=col[12].get_text()
        skaterDict[name]='{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(name,pos,yr,gp,g,a,pts,pim,p_m)
    
    playerToFind=playerToFind.upper()
    statLine=''
    for goalie in goalieDict.keys():
        if(re.match(".*"+playerToFind.upper()+".*",goalie.upper())):
            statLine+=goalieDict[goalie]
    if(statLine==''):
        for skater in skaterDict.keys():
            if(re.match(".*"+playerToFind.upper()+".*",skater.upper())):
                statLine+=skaterDict[skater]
    else:
        return "```\n" + goalieHeader + statLine + "```"
    if(statLine==''):
        return "Player Not Found"
    else:
        return "```\n" + skaterHeader + statLine + "```"
def getHEPI(gender):
    url = "http://hockeyeastonline.com/{}/standings/index.php".format(gender)
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    tab = soup.find_all("table",{'class':'story-table'})
    rows=tab[0].find_all('tr')
    rankings='```\n'
    for i in range(2,len(rows)):
        col=rows[i].find_all('td')
        rankings+=("{}. {}\t{}\n".format(col[0].get_text(),col[1].get_text(),col[2].get_text()))
    rankings+='```'
    return rankings
    
def generateScoreline(team, gender):
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
    gameList = []
    nextbutton = soup.find('a',{'class':'button2 next'})
    now = datetime.datetime.now()
    if(nextbutton.get_text() == 'Today'  and now.hour>4):
        url = "https://www.collegehockeynews.com/{}".format(nextbutton['href'])
        f=urllib.request.urlopen(url,timeout=10)
        html = f.read()
        f.close()
        soup = BeautifulSoup(html, 'html.parser')
        data =soup.find_all('div',{'class':'confGroup'})
        
    if(team in chnDiffs.keys()):
        team=chnDiffs[team]
    if not scorebot.isD1(team,team,gender) and not team in chnDiffs.values():
        return ":regional_indicator_x: Team Not Found"
    for conf in data:
        conference=conf.find('h2').get_text()
        games=conf.find_all('table',{'id':'mainscore'})
        for i in games:

            gameData=i.find_all('td')
            if(len(gameData)>=8):
                awayTeam=gameData[2].get_text()
                awayScore=gameData[3].get_text()
                homeTeam=gameData[7].get_text()
                homeScore=gameData[8].get_text()
                status=gameData[4].get_text(separator=" ")
            if(len(gameData)==7):
                awayTeam=gameData[1].get_text()
                awayScore=gameData[2].get_text()
                homeTeam=gameData[5].get_text()
                homeScore=gameData[6].get_text()
                status=gameData[3].get_text(separator=" ")
            
            if(team==homeTeam or team==awayTeam):
                if(awayTeam in flairlist):
                    awayTeam = flairlist[awayTeam] + " " + awayTeam
                if(homeTeam in flairlist):
                    homeTeam = flairlist[homeTeam] + " " + homeTeam
                scoreline= "{} {}\n{} {}\n{}".format(awayTeam,awayScore,homeTeam,homeScore,status)
                return scoreline
    return "No game scheduled for {} {}".format(team,gender)

def generatePDOPlot(gender):
    if(gender=='Mens'):
        url = "https://www.collegehockeynews.com/stats/"
        svFileName = '/home/nmemme/discordBot/pdoplotdata/sv_data.txt'
        pdoPlotName ='/home/nmemme/discordBot/pdoplotdata/pdoplot.png'
    if(gender=='Womens'):
        url = "https://www.collegehockeynews.com/women/stats.php"
        svFileName = '/home/nmemme/discordBot/pdoplotdata/w_sv_data.txt'
        pdoPlotName ='/home/nmemme/discordBot/pdoplotdata/wpdoplot.png'
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    logoDict={"Air Force" : "images/logos/afa.png",
            "Alabama Huntsville" : "images/logos/alh.png",
            "Alaska Anchorage" : "images/logos/aka.png",
            "Alaska" : "images/logos/akf.png",
            "American Int'l" : "images/logos/aic.png",
            "Arizona State" : "images/logos/asu.png",
            "Army" : "images/logos/arm.png",
            "Bemidji State" : "images/logos/bmj.png",
            "Bentley" : "images/logos/ben.png",
            "Boston College" : "images/logos/bc_.png",
            "Boston University" : "images/logos/bu_.png",
            "Bowling Green" : "images/logos/bgs.png",
            "Brown" : "images/logos/brn.png",
            "Canisius" : "images/logos/cns.png",
            "Clarkson" : "images/logos/clk.png",
            "Colgate" : "images/logos/clg.png",
            "Colorado College" : "images/logos/cc_.png",
            "Cornell" : "images/logos/cor.png",
            "Dartmouth" : "images/logos/dar.png",
            "Denver" : "images/logos/den.png",
            "Ferris State" : "images/logos/fsu.png",
            "Franklin Pierce" : "images/logos/fpu.png",
            "Harvard" : "images/logos/har.png",
            "Holy Cross" : "images/logos/hcr.png",
            "Lake Superior" : "images/logos/lss.png",
            "Lindenwood" : "images/logos/lin.png",
            "Long Island" : "images/logos/liu.png",
            "Maine" : "images/logos/mne.png",
            "Massachusetts" : "images/logos/uma.png",
            "Mercyhurst" : "images/logos/mrc.png",
            "Merrimack" : "images/logos/mer.png",
            "Miami" : "images/logos/mia.png",
            "Michigan State" : "images/logos/msu.png",
            "Michigan Tech" : "images/logos/mtu.png",
            "Michigan" : "images/logos/mic.png",
            "Minnesota-Duluth" : "images/logos/mnd.png",
            "Minnesota State" : "images/logos/mns.png",
            "Minnesota" : "images/logos/min.png",
            "New Hampshire" : "images/logos/unh.png",
            "Niagara" : "images/logos/nia.png",
            "North Dakota" : "images/logos/ndk.png",
            "Northeastern" : "images/logos/noe.png",
            "Northern Michigan" : "images/logos/nmu.png",
            "Notre Dame" : "images/logos/ndm.png",
            "Ohio State" : "images/logos/osu.png",
            "Omaha" : "images/logos/uno.png",
            "Penn State" : "images/logos/psu.png",
            "Post" : "images/logos/pst.png",
            "Princeton" : "images/logos/prn.png",
            "Providence" : "images/logos/prv.png",
            "Quinnipiac" : "images/logos/qui.png",
            "RIT" : "images/logos/rit.png",
            "Rensselaer" : "images/logos/ren.png",
            "Robert Morris" : "images/logos/rmu.png",
            "Sacred Heart" : "images/logos/sac.png",
            "Saint Anselm" : "images/logos/sta.png",
            "Saint Michael's" : "images/logos/stm.png",
            "St. Cloud State" : "images/logos/stc.png",
            "St. Lawrence" : "images/logos/stl.png",
            "St. Thomas" : "images/logos/stt.png",
            "Syracuse" : "images/logos/syr.png",
            "Connecticut" : "images/logos/con.png",
            "Mass.-Lowell" : "images/logos/uml.png",
            "Union" : "images/logos/uni.png",
            "Vermont" : "images/logos/ver.png",
            "Western Michigan" : "images/logos/wmu.png",
            "Wisconsin" : "images/logos/wis.png",
            "Yale" : "images/logos/yal.png"}
            
    standStats=soup.find('table',{'id':'standard'})
    thead=standStats.find('thead')
    headers = thead.find_all('th')
    headers = [i.get_text() for i in headers]
    tbod=standStats.find('tbody')
    statDict = {}

    for row in tbod.find_all('tr'):
        col = row.find_all('td')
        teamDict ={}
        for i in range(len(col)):
            val = col[i].get_text()
            if(val.isnumeric() or val.replace('.', '', 1).isdigit()):
                val=float(val)
               
            teamDict[headers[i]] = val
        
        statDict[col[1].get_text()] = teamDict 

    sv=[]
    sh=[]
    marker=[]
    for i in statDict.keys():
        sv.append(statDict[i]['SV%'])
        sh.append(statDict[i]['Sh%'])
        marker.append(i)

    newData=False

    if (os.path.exists(svFileName)):
        foname = open(svFileName,'r')
        counter=0
        for i in foname:
            if(sv[counter]!=float(i.rstrip('\n'))):            
                newData=True
                break
            counter+=1
        foname.close()
        
    else:
        newData = True   
        fname = open(svFileName,'w')
        for i in sv:
            print(i,file=fname)
        fname.close()

    if(newData or (not os.path.exists(pdoPlotName))):
        fname = open(svFileName,'w')
        for i in sv:
            print(i,file=fname)
        fname.close()
        for team in statDict.keys():
            statDict[team]['logo'] = "https://www.collegehockeynews.com/"+logoDict[team]
            statDict[team]['img'] = imageio.imread(urllib.request.urlopen(statDict[team]['logo']).read())


        plt.rcParams["figure.figsize"] = [9, 9]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('lightgray')
        fig.patch.set_alpha(1)
        for x0, y0, path in zip(sh, sv, marker):
           ab = AnnotationBbox(OffsetImage(statDict[path]['img'], zoom=.1), (x0, y0), frameon=False)
           ax.add_artist(ab)
        plt.xticks(np.arange(round(min(sh),2)-1,max(sh)+1))
        plt.yticks(np.arange(round(min(sv),2)-.01,max(sv)+.01,.02))
        plt.ylim([min(sv),max(sv)])
        plt.xlim([min(sh),max(sh)])
        plt.xlabel('Sh%')
        plt.ylabel('Sv%')
        plt.title('PDO Breakdown')
        plt.vlines(np.mean(sh),plt.ylim()[0],plt.ylim()[1])
        plt.hlines(np.mean(sv),plt.xlim()[0],plt.xlim()[1])
        plt.text(plt.xlim()[0]+.2,plt.ylim()[1]-.01,'Dull',fontsize=15,color='gray')
        plt.text(plt.xlim()[1]-1.5,plt.ylim()[1]-.01,'Lucky',fontsize=15,color='gray')
        plt.text(plt.xlim()[0]+.2,plt.ylim()[0]+.01,'Unlucky',fontsize=15,color='gray')
        plt.text(plt.xlim()[1]-1.5,plt.ylim()[0]+.01,'Fun',fontsize=15,color='gray')
        plt.grid()
        plt.savefig(pdoPlotName)

    return pdoPlotName
    
def generateCorsiPlot(gender):
    if(gender=='Mens'):
        url = "https://www.collegehockeynews.com/stats/"
        cfFileName = '/home/nmemme/discordBot/pdoplotdata/cf_data.txt'
        corsiFileName = '/home/nmemme/discordBot/pdoplotdata/corsiplot.png'
    if(gender=='Womens'):
        url = "https://www.collegehockeynews.com/women/stats.php"
        cfFileName = '/home/nmemme/discordBot/pdoplotdata/wcf_data.txt'
        corsiFileName ='/home/nmemme/discordBot/pdoplotdata/wcorsiplot.png'
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    logoDict={"Air Force" : "images/logos/afa.png",
            "Alabama Huntsville" : "images/logos/alh.png",
            "Alaska Anchorage" : "images/logos/aka.png",
            "Alaska" : "images/logos/akf.png",
            "American Int'l" : "images/logos/aic.png",
            "Arizona State" : "images/logos/asu.png",
            "Army" : "images/logos/arm.png",
            "Bemidji State" : "images/logos/bmj.png",
            "Bentley" : "images/logos/ben.png",
            "Boston College" : "images/logos/bc_.png",
            "Boston University" : "images/logos/bu_.png",
            "Bowling Green" : "images/logos/bgs.png",
            "Brown" : "images/logos/brn.png",
            "Canisius" : "images/logos/cns.png",
            "Clarkson" : "images/logos/clk.png",
            "Colgate" : "images/logos/clg.png",
            "Colorado College" : "images/logos/cc_.png",
            "Cornell" : "images/logos/cor.png",
            "Dartmouth" : "images/logos/dar.png",
            "Denver" : "images/logos/den.png",
            "Ferris State" : "images/logos/fsu.png",
            "Franklin Pierce" : "images/logos/fpu.png",
            "Harvard" : "images/logos/har.png",
            "Holy Cross" : "images/logos/hcr.png",
            "Lake Superior" : "images/logos/lss.png",
            "Lindenwood" : "images/logos/lin.png",
            "Long Island" : "images/logos/liu.png",
            "Maine" : "images/logos/mne.png",
            "Massachusetts" : "images/logos/uma.png",
            "Mercyhurst" : "images/logos/mrc.png",
            "Merrimack" : "images/logos/mer.png",
            "Miami" : "images/logos/mia.png",
            "Michigan State" : "images/logos/msu.png",
            "Michigan Tech" : "images/logos/mtu.png",
            "Michigan" : "images/logos/mic.png",
            "Minnesota-Duluth" : "images/logos/mnd.png",
            "Minnesota State" : "images/logos/mns.png",
            "Minnesota" : "images/logos/min.png",
            "New Hampshire" : "images/logos/unh.png",
            "Niagara" : "images/logos/nia.png",
            "North Dakota" : "images/logos/ndk.png",
            "Northeastern" : "images/logos/noe.png",
            "Northern Michigan" : "images/logos/nmu.png",
            "Notre Dame" : "images/logos/ndm.png",
            "Ohio State" : "images/logos/osu.png",
            "Omaha" : "images/logos/uno.png",
            "Penn State" : "images/logos/psu.png",
            "Post" : "images/logos/pst.png",
            "Princeton" : "images/logos/prn.png",
            "Providence" : "images/logos/prv.png",
            "Quinnipiac" : "images/logos/qui.png",
            "RIT" : "images/logos/rit.png",
            "Rensselaer" : "images/logos/ren.png",
            "Robert Morris" : "images/logos/rmu.png",
            "Sacred Heart" : "images/logos/sac.png",
            "Saint Anselm" : "images/logos/sta.png",
            "Saint Michael's" : "images/logos/stm.png",
            "St. Cloud State" : "images/logos/stc.png",
            "St. Lawrence" : "images/logos/stl.png",
            "St. Thomas" : "images/logos/stt.png",
            "Syracuse" : "images/logos/syr.png",
            "Connecticut" : "images/logos/con.png",
            "Mass.-Lowell" : "images/logos/uml.png",
            "Union" : "images/logos/uni.png",
            "Vermont" : "images/logos/ver.png",
            "Western Michigan" : "images/logos/wmu.png",
            "Wisconsin" : "images/logos/wis.png",
            "Yale" : "images/logos/yal.png"}
            
    advStats=soup.find('table',{'id':'advanced'})
    tbod=advStats.find('tbody')
    aHeaders=['Rk','Team','GP','SATTOT','SATATOT','CF%TOT','SATEV','SATAEV','CF%EV','SATPP','SATAPP','CF%PP','SATCL','SATACL','CF%CL']
    statDict={}
    for row in tbod.find_all('tr'):
        col=row.find_all('td',{'class':None})
        col+=(row.find_all('td',{'class':'t c'}))
        teamDict ={}
        for i in range(len(col)):
            val = col[i].get_text()
            if(val.isnumeric() or val.replace('.', '', 1).isdigit()):
                val=float(val)
               
            teamDict[aHeaders[i]] = val
        statDict[col[1].get_text()] = teamDict 

    cf=[]
    ca=[]
    marker=[]
    for i in statDict.keys():
        cf.append(statDict[i]['SATEV']/statDict[i]['GP'])
        ca.append(statDict[i]['SATAEV']/statDict[i]['GP'])
        marker.append(i)
        

    newData=False
    if (os.path.exists(cfFileName)):
        foname = open(cfFileName,'r')
        counter=0
        for i in foname:
            if(cf[counter]!=float(i.rstrip('\n'))):  
                newData=True
                break
            counter+=1
        foname.close()
        
    else:
        newData = True   
        fname = open(cfFileName,'w')
        for i in cf:
            print(i,file=fname)
        fname.close()

    if(newData or (not os.path.exists(corsiFileName))):
        fname = open(cfFileName,'w')
        for i in cf:
            print(i,file=fname)
        fname.close()
        for team in statDict.keys():
            statDict[team]['logo'] = "https://www.collegehockeynews.com/"+logoDict[team]
            statDict[team]['img'] = imageio.imread(urllib.request.urlopen(statDict[team]['logo']).read())

        plt.rcParams["figure.figsize"] = [9, 9]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('lightgray')
        fig.patch.set_alpha(1)
        for x0, y0, path in zip(cf, ca, marker):
           ab = AnnotationBbox(OffsetImage(statDict[path]['img'], zoom=.1), (x0, y0), frameon=False)
           ax.add_artist(ab)
        plt.xticks(np.arange(round(min(cf))-1,max(cf)+1,5))
        plt.yticks(np.arange(round(min(ca))-1,max(ca)+1,5))
        plt.ylim([max(ca)+1,min(ca)-1])
        plt.xlim([min(cf)-1,max(cf)+1])
        plt.xlabel('Cf/60')
        plt.ylabel('Ca/60')
        plt.title('Team Shot Rates')
        plt.vlines(np.mean(ca),plt.ylim()[0],plt.ylim()[1])
        plt.hlines(np.mean(cf),plt.xlim()[0],plt.xlim()[1])
        plt.text(plt.xlim()[0]+2,plt.ylim()[1]+2,'Dull',fontsize=15,color='gray')
        plt.text(plt.xlim()[1]-5,plt.ylim()[1]+2,'Good',fontsize=15,color='gray')
        plt.text(plt.xlim()[0]+2,plt.ylim()[0]-2,'Bad',fontsize=15,color='gray')
        plt.text(plt.xlim()[1]-5,plt.ylim()[0]-2,'Fun',fontsize=15,color='gray')
        plt.grid()
        plt.savefig(corsiFileName)

    return corsiFileName
    
def getTransitiveWinChain(team1,team2):
    if(team1 == '' or team2 == ''):
        return "Enter Two Teams!"
    
    global chnDiffs
 
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
        
    url = "https://www.collegehockeynews.com/schedules/composite.php"
    f=urllib.request.urlopen(url)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    games= soup.find('pre')
    LossDict={}
    gList=games.get_text().split('\n')
    for i in gList:
        m=re.search(r"^(\S*) (\S* ?\S* \S*)\s*(\S*) (?:at|vs) (\S* ?\S* \S*)\s*(\S*)\s*(\S*)  ([a-z]*)",i)
        if(m.group(3)==''):
            break
        aTeam=m.group(2).rstrip(' ')
        aScore=int(m.group(3))
        hTeam=m.group(4).rstrip(' ')
        hScore=int(m.group(5))
        if(m.group(6)=='ot'):
            conf=m.group(7)
        else:
            conf=m.group(6) 
        if(conf=='ex'):
            continue
        if(aScore<hScore):
            if(hTeam not in LossDict.keys()):
                LossDict[hTeam]=set()
                LossDict[hTeam].add(aTeam)
            else:
                LossDict[hTeam].add(aTeam)
        elif(aScore>hScore):
            if(aTeam not in LossDict.keys()):
                LossDict[aTeam]=set()
                LossDict[aTeam].add(hTeam)
            else:
                LossDict[aTeam].add(hTeam)
    
    G=nx.DiGraph(LossDict,directed=True)
    try:
        shortPath=nx.algorithms.shortest_path(G,team1,team2)
    except:
        return "```No Win Chains Found```"
    pathStr=''
    for i in range(len(shortPath)):
        pathStr+=shortPath[i]
        if(i<len(shortPath)-1):
            pathStr+=' > '
    return '```\n'+pathStr+'```'
client.run(TOKEN)
print("Ending... at",datetime.datetime.now())
