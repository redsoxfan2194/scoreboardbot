import random
import discord
from time import strftime,localtime
import json
import random
import ast

invalidRoles = ['@everyone', 'Mods', 'Admin', 'bot witch', 'Dyno', 'CH_Scorebot','color moderator']


def loadCmds():
    cmdDict={}
    with open('/home/nmemme/ch_scorebot/discordBot/rCHCmds/rCollegeHockeyCmds.json', 'r') as file:
        cmdDict=json.load(file)
    return cmdDict
    
def addCmd(cmd,res):
  global cmdDict
  cmd = cmd.strip()
  res = res.strip()
  if cmd in cmdDict.keys():
      cmdDict[cmd].append(res)
  else:
      cmdDict[cmd]=[]
      cmdDict[cmd].append(res)
  cmdDict[cmd] = list(set(cmdDict[cmd]))
  with open('/home/nmemme/ch_scorebot/discordBot/rCHCmds/rCollegeHockeyCmds.json', 'w') as file:
      file.write(json.dumps(cmdDict))
  return f"'{res}' added to '?{cmd}'"
  
def rmCmd(cmd):
    global cmdDict
    if cmd in cmdDict.keys():
        cmdDict.pop(cmd)
    with open('/home/nmemme/ch_scorebot/discordBot/rCHCmds/rCollegeHockeyCmds.json', 'w') as file:
        file.write(json.dumps(cmdDict))
    return f"?{cmd} removed"

def findCmd(cmd):
    global cmdDict
    cmd=cmd.strip('?')
    if cmd in cmdDict.keys():
        if(len(cmdDict[cmd])>1):
          return random.choice(cmdDict[cmd])
        else:
          return cmdDict[cmd][0]
    return ''

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
        "au" : "Augustana",
        "augie" : "Augustana",
        "amworst" : "Massachusetts",
        "amwurst" : "Massachusetts",
        "anosu" : "Ohio State",
        "army" : "Army West Point",
        "asu" : "Arizona State",
        "bama" : "Alabama Huntsville",
        "babyshark":"Long Island",
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
        "ud" : "Delaware",
        "du" : "Denver",
        "duluth" : "Minnesota Duluth",
        "ferris" : "Ferris State",
        "ferriswheel" : "Ferris State",
        "finghawks" : "North Dakota",
        "fp" : "Franklin Pierce",
        "goofers" : "Minnesota",
        "hc" : "Holy Cross",
        "hu" : "Harvard",
        "homeless" : "Northeastern",
        "thehomeless" : "Northeastern",
        "homelesshuskies" : "Northeastern",
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
        "maryville" : "Maryville Saints",
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
        "rpi" : "RPI",
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
        "tecc" : "Michigan Tech",
        "tsu" : "Tennessee State",
        "uaa" : "Alaska Anchorage",
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

cmdDict = loadCmds()

def rCollegeHockeyAdmin(message):
  global cmdDict
  ret=[]
  
  if(message.content.startswith('?addcmd ') and message.channel.name == 'bot-test'):
    cmdList = message.content.split('?addcmd ')
    if(len(cmdList)<2):
      ret.append(message.channel.send("Please input two comma separated values"))
    else:
      cmdSplit=cmdList[1].split(',',maxsplit=1)
      ret.append(message.channel.send(addCmd(cmdSplit[0],cmdSplit[1])))
    return ret
  if(message.content.startswith('?rmcmd ') and message.channel.name == 'bot-test'):
    cmdList = message.content.split('?rmcmd ')
    if(len(cmdList)==1):
      ret.append(message.channel.send("Please input a cmd to remove"))
    ret.append(message.channel.send(rmCmd(cmdList[1].strip())))
    cmdDict=loadCmds()
    return ret
  if(message.content.startswith('?roles')):
        try:
            roleChoice = message.content.split('?roles ')
            if(len(roleChoice)==1):
                    
                roles1 = "```"
                roles2 = "```"
                rList= message.guild.roles
                if(len(rList)>1):
                  half1 = rList[len(rList)//2:]
                  half2 = rList[:len(rList)//2]
                for i in half1:
                    if(i.name not in invalidRoles):
                        roles1+= i.name + "\n"
                if(roles1 != "```\n"):
                    roles1 += '```'
                    ret.append(message.author.send(roles1))
                for i in half2:
                    if(i.name not in invalidRoles):
                        roles2+= i.name + "\n"
                if(roles2 != "```\n"):
                    roles2 += '```'
                    ret.append(message.author.send(roles2))
            else:
                for i in message.guild.roles:
                  if(roleChoice[1] == i.name.lower() and roleChoice[1] not in invalidRoles):
                    user=message.author
                    ret.append(user.add_roles(i))
                    ret.append(message.channel.send("{} added to {}".format(i.name, message.author.mention)))
                    return ret
                team=convertTeamtoDisRole(decodeTeam(roleChoice[1]))
                if(team==''):
                    team=roleChoice[1]
                if(team not in invalidRoles):
                    roleFound=False
                    ret = []
                    for i in message.guild.roles:
                        if(team == i.name):   
                            user=message.author
                            ret.append(user.add_roles(i))
                            ret.append(message.channel.send("{} added to {}".format(team, message.author.mention)))
                            roleFound=True
                            break
                    
                    if(not roleFound):
                        ret.append(message.channel.send("Invalid Role"))
                    return ret
                else:
                    ret.append(message.channel.send("Invalid Role"))
            return ret
        except discord.errors.Forbidden:
            ret.append(message.channel.send("Invalid Role"))
            return ret
  if(message.content.startswith('?rroles')):
        roleChoice = message.content.split('?rroles ')
        ret = []
        try:
            if(len(roleChoice)==1):
                ret.append(message.channel.send("Enter a Role to Remove"))
            else:
                for i in message.guild.roles:
                  if(roleChoice[1] == i.name.lower() and roleChoice[1] not in invalidRoles):
                    user=message.author
                    ret.append(user.remove_roles(i))
                    ret.append(message.channel.send("{} removed from {}".format(i.name, message.author.mention)))
                    return ret
                team=convertTeamtoDisRole(decodeTeam(roleChoice[1]))
                if(team==''):
                    team=roleChoice[1]
                if(team not in invalidRoles):
                    roleFound=False
                    for i in message.guild.roles:
                        ret = []
                        if(team == i.name):   
                            user=message.author
                            ret.append(user.remove_roles(i))
                            ret.append(message.channel.send("{} removed from {}".format(team, message.author.mention)))
                            roleFound=True
                            break
                            
                    if(not roleFound):
                        ret.append(message.channel.send("Invalid Role"))
                    return ret
                else:
                    ret.append(message.channel.send("Invalid Role"))
                    return ret
        except discord.errors.Forbidden:
            ret.append(message.channel.send("Invalid Role"))
            return ret
  
def rCollegeHockeyMemesAndGifs(message):

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
            msg = "I don't know that cheer."
            if(convertTeamtoDisRole(team) != ""):
                teamName = convertTeamtoDisRole(team)
                msg = "Go {}!".format(teamName)
        if(msg!="I don't know that cheer."): 
          return message.channel.send(msg)
        
    if message.content.startswith('?jeer '):
        teamChoice = message.content.split('?jeer ')
        jeer = ""
        if(len(teamChoice)>1):
            team=decodeTeam(teamChoice[1])
            jeer = getJeer(convertTeamtoDisRole(team))
            
        if(jeer!=""):
            msg="{}".format(jeer)
        else:
            msg = "I don't know that jeer."
            teamName=team
            if(convertTeamtoDisRole(team) != ""):
                teamName = convertTeamtoDisRole(team)
                msg = "Boo {}".format(teamName)
        if(msg!="I don't know that jeer."):
          return message.channel.send(msg)
        
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
            teamName=team
            if(convertTeamtoDisRole(team) != ""):
                teamName = convertTeamtoDisRole(team)
                msg = "Boo {}".format(teamName)
        if(msg != "I don't know that jeer."):
          return message.channel.send(msg)
        
  # gifs and stuff
    msg = findCmd(message.content)
    if(msg != ''):
      return message.channel.send(msg)
       
    if(message.content.startswith('?recruit')):
      teamChoice = message.content.split('?recruit ')
      if(len(teamChoice)>1):
          team=decodeTeam(teamChoice[1])
          if(team=='Rensselaer'):
              team='RPI'
          cheer = getCheer(convertTeamtoDisRole(team))
          if(cheer==""):
              team="NO TEAM"
      elif(len(teamChoice)==1):
          for i in range(len(message.author.roles)):
              if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch" and message.author.roles[-1-i].name !=  "Craig"):
                  team = convertDisRoleToTeam(message.author.roles[-1-i].name)
                  break
      else:
          team='[Insert Team Rooting For Here]'    
          
      if(team!="NO TEAM"):
        return message.channel.send("This is a good option for {} to pursue.  They should target him.".format(team))
  
    if(message.content.startswith('?wrecruit')):
      teamChoice = message.content.split('?wrecruit ')
      if(len(teamChoice)>1):
          team=decodeTeam(teamChoice[1])
          if(team=='Rensselaer'):
              team='RPI'
          cheer = getCheer(convertTeamtoDisRole(team))
          if(cheer==""):
              team="NO TEAM"
      elif(len(teamChoice)==1):
          for i in range(len(message.author.roles)):
              if(message.author.roles[-1-i].name !=  "Mods" and message.author.roles[-1-i].name !=  "Admin" and message.author.roles[-1-i].name !=  "Georgia Tech Yellow Jackets" and message.author.roles[-1-i].name !=  "TEAM CHAOS" and message.author.roles[-1-i].name !=  "bot witch" and message.author.roles[-1-i].name !=  "Craig"):
                  team = convertDisRoleToTeam(message.author.roles[-1-i].name)
                  break
      else:
          team='[Insert Team Rooting For Here]'    
      if(team!="NO TEAM"):
        return message.channel.send("This is a good option for {} to pursue.  They should target her.".format(team))
      

def convertTeamtoDisRole(team):

    teams = { "Air Force" : "Air Force Falcons",
                "Alabama Huntsville" : "Alabama Huntsville Chargers",
                "Alaska" : "Alaska Nanooks",
                "Alaska Anchorage" : "Alaska-Anchorage Seawolves",
                "American International" : "American International Yellow Jackets",
                "Augustana" : "Augustana Vikings",
                "Assumption" : "Assumption Greyhounds",
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
                "Delaware" : "Delaware Fightin' Blue Hens",
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
                "Maryville" : "Maryville Saints",
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
                "RPI" : "RPI Engineers",
                "Robert Morris" : "Robert Morris Colonials",
                "Sacred Heart" : "Sacred Heart Pioneers",
                "Stonehill" : "Stonehill Skyhawks",
                "Sieve" : "Sieve",
                "Craig" : "Craig",
                "Politics" : "Political Discussion",
                "Gambling" : "Gambling Chat",
                "Voter" : "/r/collegehockey Poll Voter",
                "St. Anselm" : "St. Anselm Hawks",
                "St. Cloud State" : "St. Cloud State Huskies",
                "St. Lawrence" : "St. Lawrence Saints",
                "St. Michael's" : "St. Michael's Purple Knights",
                "Saint Michael's" : "St. Michael's Purple Knights",
                "Syracuse" : "Syracuse Orange",
                "Tennessee State" : "Tennessee State Tigers",
                "UConn" : "UConn Huskies",
                "UMass Lowell" : "UMass Lowell River Hawks",
                "Massachusetts" : "UMass Minutemen",
                "Union" : "Union Garnet Chargers",
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
                "Jackbox" : "Jackbox Game Night",
                "USA" : "USA",
                "Chaos" : "TEAM CHAOS"}
                
    if team in teams:
        return teams[team]
    elif team in teams.values():
        return team
    else:
        return ""
        
def convertDisRoleToTeam(team):
    teams = {   "Air Force Falcons" : "Air Force",
                "Alabama Huntsville Chargers" : "Alabama Huntsville",
                "Alaska Nanooks" : "Alaska",
                "Alaska-Anchorage Seawolves" : "Alaska Anchorage",
                "American International Yellow Jackets" : "American International",
                "Arizona State Sun Devils" : "Arizona State",
                "Army Black Knights" : "Army West Point",
                "Assumption Greyhounds" : "Assumption",
                "Augustana Vikings" : "Augustana",
                "Bemidji State Beavers" : "Bemidji State",
                "Bentley Falcons" : "Bentley",
                "Boston College Eagles" : "Boston College",
                "Boston University Terriers" : "Boston University",
                "Bowling Green Falcons" : "Bowling Green",
                "Brown Bears" : "Brown",
                "Canisius Golden Griffins" : "Canisius",
                "Clarkson Golden Knights" : "Clarkson",
                "Colgate Raiders" : "Colgate",
                "Colorado College Tigers" : "Colorado College",
                "Cornell Big Red" : "Cornell",
                "Dartmouth Big Green" : "Dartmouth",
                "Delaware Fightin' Blue Hens" : "Delaware",
                "Denver Pioneers" : "Denver",
                "Ferris State Bulldogs" : "Ferris State",
                "Franklin Pierce Ravens" : "Franklin Pierce",
                "Georgia Tech Yellow Jackets" : "Georgia Tech",
                "Harvard Crimson" : "Harvard",
                "Holy Cross Crusaders" : "Holy Cross",
                "Lake Superior State Lakers" : "Lake Superior State",
                "Lindenwood Lions" : "Lindenwood",
                "LIU Sharks" : "Long Island University",
                "Maine Black Bears" : "Maine",
                "Maryville Saints" : "Maryville",
                "Mercyhurst Lakers" : "Mercyhurst",
                "Merrimack Warriors" : "Merrimack",
                "Miami RedHawks" : "Miami",
                "Michigan State Spartans" : "Michigan State",
                "Michigan Tech Huskies" : "Michigan Tech",
                "Michigan Wolverines" : "Michigan",
                "Minnesota Duluth Bulldogs" : "Minnesota Duluth",
                "Minnesota Golden Gophers" : "Minnesota",
                "Minnesota State Mavericks" : "Minnesota State",
                "New Hampshire Wildcats" : "New Hampshire",
                "Niagara Purple Eagles" : "Niagara",
                "North Dakota Fighting Hawks" : "North Dakota",
                "Northeastern Huskies" : "Northeastern",
                "Northern Michigan Wildcats" : "Northern Michigan",
                "Notre Dame Fighting Irish" : "Notre Dame",
                "Ohio State Buckeyes" : "Ohio State",
                "Omaha Mavericks" : "Omaha",
                "Penn State Nittany Lions" : "Penn State",
                "Post Eagles" : "Post",
                "Princeton Tigers" : "Princeton",
                "Providence Friars" : "Providence",
                "Quinnipiac Bobcats" : "Quinnipiac",
                "RIT Tigers" : "RIT",
                "RPI Engineers" : "RPI",
                "Robert Morris Colonials" : "Robert Morris",
                "Sacred Heart Pioneers" : "Sacred Heart",
                "Stonehill Skyhawks" : "Stonehill",
                "Sieve" : "Sieve",
                "Craig" : "Craig",
                "/r/collegehockey Poll Voter" : "Voter",
                "St. Anselm Hawks" : "St. Anselm",
                "St. Cloud State Huskies" : "St. Cloud State",
                "St. Lawrence Saints" : "St. Lawrence",
                "St. Michael's Purple Knights" : "St. Michael's",
                "Syracuse Orange" : "Syracuse",
                "Tennessee State Tigers" : "Tennessee State",
                "UConn Huskies" : "UConn",
                "UMass Lowell River Hawks" : "UMass Lowell",
                "UMass Minutemen" : "Massachusetts",
                "Union Garnet Chargers" : "Union",
                "Vermont Catamounts" : "Vermont",
                "Western Michigan Broncos" : "Western Michigan",
                "Wisconsin Badgers" : "Wisconsin",
                "Yale Bulldogs" : "Yale",
                "Louisiana Ragin' Cajuns" : "UL Lafayette",
                "Louisiana State University Tigers" : "LSU",
                "Georgia Tech Yellow Jackets" : "Georgia Tech",
                "St. Thomas Tommies" : "St. Thomas",
                "Ref" : "Ref",
                "Meteor" : "Meteor",
                "Portal" : "Portal",
                "Jackbox Game Night" : "Jackbox",
                "USA" : "USA",
                "TEAM CHAOS" : "Chaos",
                "color cornell" :"Cornell",
                "color maine" : "Maine",
                "color princeton" : "Princeton",
                "color vermont" :  "Vermont",
                "color maine" :  "Maine",
                "color wisconsin" : "Wisconsin",
                "color north dakota" : "North Dakota",
                "color michigan state" : "Michigan State",
                "color michigan tech" : "Michigan Tech",
                "color lowell" : "UMass Lowell",
                "color quinnipiac" : "Quinnipiac"}
                
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
    elif(role == "color michigan state"):
        role = "Michigan State Spartans"
    elif(role == "color lowell"):
        role = "UMass Lowell River Hawk"
    elif(role == "color michigan tech"):
        role = "Michigan Tech Huskies"
    elif(role == "color quinnipiac"):
        role = "Quinnipiac Bobcats"
    cheerList = { "Boston University Terriers" : ["Go BU!", "Let's Go Terriers!", "BC Sucks!"],
    "Northeastern Huskies" : ["Go NU!", "#HowlinHuskies", "Go Huskies!"],
    "Cornell Big Red" : ["Let's Go Red!", "Go Big Red!", "Fuck Harvard!", "Screw BU!"],
    "Harvard Crimson" : ["Go Harvard!", "Fuck Harvard!", "Go Crimson!"],
    "New Hampshire Wildcats" : ["I Believe in UNH!","Go Wildcats!"],
    "Maine Black Bears" : ["Let's go Black Bears!", "Fill the steins to Dear Ol' Maine!"],
    "Boston College Eagles" : ["Go BC!", "BC Sucks!", "Go Eagles!", "Sucks to BU!"],
    "UMass Minutemen" : ["Go Amherst!", "Go U Mass!"],
    "UConn Huskies" : ["Go Huskies!", "U-C-O-N-N UCONN UCONN UCONN", "Ice Bus"],
    "Union Garnet Chargers" : ["Let's Go U!"],
    "Michigan Tech Huskies" : ["Go Huskies!","Hecc Yeah Tecc!"],
    "UMass Lowell River Hawks" : ["Go River Hawks!"],
    "Lake Superior State Lakers" : ["Ringy Dingy!"],
    "Bemidji State Beavers" : ["Roll Dam Beavs!", "Go Beavs!", "Go Beavers!"],
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
    "Western Michigan Broncos" : ["Go Broncos!", "Let's Ride", "#StanHorsies"],
    "TEAM CHAOS": ["CHAOS REIGNS"],
    "Meteor" : ["https://media.tenor.com/images/892268e557475c225acebe707c85bffc/tenor.gif"],
    "Portal" : ["PRAISE PORTAL"],
    "Craig" : ["https://media.discordapp.net/attachments/279688498485919744/1028033049260216370/Screenshot_20221007-155607_Twitter.jpg"],
    "Louisiana Ragin' Cajuns": ["Geaux Cajuns!"]}
    if role in cheerList:   
            if(role=="Boston College Eagles"):
                return random.choices(cheerList[role],weights=[60,5,90,10])[0]
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
    "Union Garnet Chargers" : ["Can't spell sucks without UC!!"],
    "Brown Bears" : ["URI Rejects!", "Brown is Shit! Shit is Brown!", "Around the bowl, down the hole, flush, flush, flush", "if it's brown, flush it down!"],
    "Princeton Tigers" : ["Rutgers Rejects!", "Princeton's in New Jerseyyy"],
    "Providence Friars" : ["https://widget.campusexplorer.com/media/original/media-7CA07320.jpg"],
    "UMass Lowell River Hawks" : ["What's a River Hawk?","Low\nLower\nLowest\nLowell"],
    "UMass Minutemen" : ["Please Don't Riot!", "We Last Longer!","Think of those couches...they have family", "Embarrassment of the Commonwealth", "https://i.imgur.com/u1SCJ73.gifv"],
    "Boston University Terriers" : ["Sucks to BU!", "Screw BU!","*A* Boston University"],
    "Northeastern Huskies" : ["Northleastern", "North! Eastern! Sucks!","https://media.discordapp.net/attachments/279689792990740481/1493991140863774780/Screenshot_20260415_110702_Discord.jpg?ex=69e0fb2c&is=69dfa9ac&hm=a6b74739c76c263c63f4262651cea44c3536b6d6c93d82d857cd641770208052&=&format=webp&width=2700&height=445","Homeless Huskies"],
    "Colgate Raiders" : ["Crest is Best!"],
    "Cornell Big Red" : ["Harvard Rejects!", "```\nUp above Cayuga's waters, there's an awful smell;\nThirty thousand Harvard rejects call themselves Cornell.\nFlush the toilet, flush the toilet,\nFlush them all to hell!\nThirty thousand Harvard rejects call themselves Cornell!```"],
    "Maine Black Bears" : ["M-A-I-N-E ~~Go Blue~~ MAAAAAIIINNNE SUCKS", "UMOwO"],
    "Louisiana State University Tigers" :["Louisiana State University and Agricultural and Mechanical College"],
    "Wisconsin Badgers" : ["Dirty Sconnies", "https://i.imgur.com/sljug4m.jpg"],
    "Michigan State Spartans" : ["Poor Sparty"],
    "Michigan Wolverines" : ["Corn Colored Cowards"],#"```\nO, we don't give a damn for the whole state of Michigan\nThe whole state of Michigan, the whole state of Michigan\nWe don't give a damn for the whole state of Michigan, we're from Ohio\nWe're from Ohio...O-H\nWe're from Ohio...I-O\nO, we don't give a damn for the whole state of Michigan\nThe whole state of Michigan, the whole state of Michigan\nWe don't give a damn for the whole state of Michigan, we're from Ohio```"],
    "Notre Dame Fighting Irish" : ["Blinded by the Light", "Notre Lame!", "Rudy was offsides!", "https://youtu.be/OCbuRA_D3KU"],
    "St. Cloud State Huskies" : ["Go back to Montreal!", "St. Cloud Sucks!", "St. Cloud is not a state"],
    "RPI Engineers" : ["KRACH is Better!"],
    "St. Lawrence Saints" : ["Sluzer"],
    "Minnesota State Mavericks" : ["Mankatno", "Mankato Sucks!"],
    "Minnesota Duluth Bulldogs" : ["Duluth Sucks!"],
    "Minnesota Golden Gophers" : ["Golden Goofs"],
    "Quinnipiac Bobcats" : ["QU PU!"],
    "Michigan Tech Huskies" : ["Tech Still Sucks!"],
    "Denver Pioneers" : ["Sucks to DU!"],
    "Ohio State Buckeyes" : ["An Ohio State University","O-H, OH NO","Another Loss for Transfer Portal U!"],
    "Arizona State Sun Devils" : ["Forked", "Fork You!", "Poor Sparky"],
    "Bowling Green Falcons" : ["Boo Ziggy", "Big Gross Stinky University"],
    "American International Yellow Jackets" : ["NO ONE JEERS MR. FUCKING. BEE."],
    "Clarkson Golden Knights" : ["It's " + strftime("%H:%M", localtime()) + " and Clarkson still sucks!"],
    "Vermont Catamounts" : ["Elephants Don't Walk That Way", "Dirty Hippies"],
    "UConn Huskies" : ["Slush Bus", "U-Cons"],
    "New Hampshire Wildcats" : ["Bad Kitty"],
    "Holy Cross Crusaders" : ["Boo Cross Boo", "Holy Cow", "No Cross No", "Moo Cow Moo"],
    "Army Black Knights" : ["Woops", "Ring Knockers", "https://www.dictionary.com/e/slang/circle-game/"],
    "Air Force Falcons" : ["Ring Knockers", "Chair Force"],
    "LIU Sharks" : ["Baby Shark Doo doo, doo doo doo doo"],
    "Penn State Nittany Lions" : ["Pennsylvania Commonwealth University"],
    "Western Michigan Broncos" : ["Broncnos"],
    "Sieve": ["Sieve, You Suck!", "Sieve! Sieve! Sieve! Sieve!", "It's All Your Fault!"],
    "Craig" : ["Imagine being named Craig"],
    "Portal" : ["Get ready for the blue bloods to purge all the talent in the game. I guarantee the next few years big schools like BC, BU, UCONN, UMASS, Michigan, Minnesota will get a boat load of talent from players who went to a smaller school and played well. These smaller schools will not be able to compete anymore because they won’t be able to offer anything these big schools can."],
    "Ref": ["I'm Blind! I'm Deaf! I wanna be a ref!", "Hey Ref, check your phone, you missed a few calls.", "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", ":regional_indicator_b: :regional_indicator_u: :regional_indicator_l: :regional_indicator_l: :regional_indicator_s: :regional_indicator_h: :regional_indicator_i: :regional_indicator_t:"]}
    if role in jeerList:
            return random.choice(jeerList[role])
    else:
        return "";
 