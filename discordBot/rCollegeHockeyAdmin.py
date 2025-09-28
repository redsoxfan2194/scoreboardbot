import random
import discord
invalidRoles = ['@everyone', 'Mods', 'Admin', 'bot witch', 'Dyno', 'CH_Scorebot','color moderator']

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

def rCollegeHockeyAdmin(message):

  if(message.content.startswith('?roles')):
        ret = []
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
                  if(roleChoice[1] == i.name and roleChoice[1] not in invalidRoles):
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
                  if(roleChoice[1] == i.name and roleChoice[1] not in invalidRoles):
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
    if(message.content.strip() == '?bu' and not (message.content.startswith('?burecbook ') or message.content.startswith('?burecordbook '))):
            return message.channel.send("https://media.giphy.com/media/mACM98U3XELWlpDxEO/giphy.mp4")
            
    if(message.content.startswith('?goodgoal')):
            return message.channel.send("https://tenor.com/view/good-goal-gif-4982175")
            
    if(message.content.startswith('?nogoal')):
            return message.channel.send("https://media.giphy.com/media/q01IxfTXuoP4Y/giphy.mp4")  

    if(message.content.startswith('?savory')):
            return message.channel.send("https://media.giphy.com/media/ozTKmmDCcE9pMNWMXF/giphy.mp4")
            
    if(message.content.startswith('?uml')):
            return message.channel.send("https://media.giphy.com/media/ejDkNiozRxVwUtbbpN/giphy.mp4")
    
    if(message.content.startswith('?lowellbu')):
            return message.channel.send("https://media.giphy.com/media/J5jccTVhlkKhogi6DP/giphy.mp4")
            
    if(message.content.startswith('?harvard')):
            return message.channel.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2JjYzk2OGMwNDZhZjY2YzlhZjFkYWQ3YWM3MWQ1NjEzMGZhM2IxYiZjdD1n/WeN7XLiKI6Gz2Pxrcc/giphy.gif")
        
    if(message.content=='?boston'):
            gif="https://m.imgur.com/ZPZUGW0"
#            random.seed(datetime.now())
#            if(random.randint(0,100)<=10):
#                gif="https://media.giphy.com/media/W2zqB99rxiTxDNT1Ci/giphy.gif"
            
            return message.channel.send(gif)
    if(message.content=='?terriers'):       
            return message.channel.send("https://imgur.com/7HQK5kU")
    if(message.content.startswith('?nuboston')):
            return message.channel.send("https://media.giphy.com/media/WU0oTNSciD83BUDfYR/giphy.gif")
            
    if(message.content.startswith('?redjd')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/680861939047333971/3pzph6.png")
    
    if(message.content.startswith('?lowell') and not message.content.startswith('?lowellbu')):
            return message.channel.send("https://imgur.com/a/C9aSorC")
            
    if(message.content.startswith('?northdakota')):
            return message.channel.send("F'IN HAWKS")
            
    if(message.content.startswith('?lane') or message.content.startswith('?hutson')):
            return message.channel.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG5nbHh2dW03YmxxaWtoZXE0ZG9jYjFtMjlyYXZ0OHIxbjMxN21zNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pKCnzx7xyJFkQSnOxd/giphy.gif")
            
    if(message.content.startswith('?jerry')):
            return message.channel.send("https://imgur.com/a/mejC6E2")
            #return message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/691772255306514552/hyW6VMD.png")
           # return message.channel.send("https://cdn.discordapp.com/attachments/523161681484972062/918644377524523008/jerry.png")
            #return message.channel.send("https://cdn.discordapp.com/attachments/523161681484972062/918854291228336148/jerry2.png") #❌❌
    
    if(message.content.startswith('?sharks') or message.content.startswith('?shorks')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279688619906826250/1312253934596788244/SHORK.png?ex=674c7bf6&is=674b2a76&hm=930afd69763f6a4c814d9af59f8b20bca06ffd73f7965e1a46dd5b3c7419b615&")
    #if(message.content.startswith('?bcot') or message.content.startswith('?❌❌ot')):
    if(message.content.startswith('?bcot')):
            return message.channel.send('"free" "hockey" in "Boston"')  
    
    if(message.content.startswith('?osutransfer')):
            return message.channel.send('ANOTHER WIN FOR TRANSFER PORTAL U')     
        
    if((message.content.startswith('?ot') and not message.content.startswith('?oti')) or message.content.startswith('?3v3ot') or message.content.startswith('?rsot') or message.content.startswith('?regularseasonot')):
            return message.channel.send('"free" "hockey"')  

    if(message.content.startswith('?oti')):
            return message.channel.send('**ON THE ICE**')    
    
    if(message.content == '?omd' or message.content == '?ea'):
            return message.channel.send('**ONE MORE DUDE**') 

    #if((message.content.startswith('?bc') and not message.content.startswith('?bcot')) or (message.content.startswith('?❌❌') and not message.content.startswith('?❌❌ot'))):
    if(message.content.startswith('?bcumass') and not message.content.startswith('?bcot')):
     
            return message.channel.send("https://media.giphy.com/media/E327kKMf0RKHAB1jpu/giphy.gif")
            
    if(message.content ==  '?bc'):
     
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1228870122672885770/lolfowler.gif?ex=662d9d7c&is=661b287c&hm=1e6a3a09f3350aca4097ae58ff1956c112cda91e6b810f009b03e5dbd1987fbd&")

    if(message.content ==  '?wbc'):
     
            return message.channel.send("https://imgur.com/sYQ27iG")
            
    if(message.content ==  '?notredame'):
     
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1219463440150827120/IMG_1270.gif?ex=66304ed4&is=661dd9d4&hm=1ff545c73c9ad66a5d297eadfa8015e25b7f685bfe9fbdf002896f34118ca09b&")
   
    if(message.content ==  '?quinnipiac'):
     
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1224470573099384852/Vinnyno.gif?ex=6622e216&is=66219096&hm=0f4d35f37ee6f339d6508171e5af843d6b422a36fb5537fa7ffcb94cd969c51a&")

    if(message.content.startswith('?eagles') or message.content.startswith('?eags')):
    
            return message.channel.send("https://imgur.com/nupbiii")
    
    if(message.content == '?uconn' ):
            return message.channel.send("https://cdn.discordapp.com/attachments/498885742802632724/1195807828544331856/EFb4oFuh.png")
            
    if(message.content.startswith('?unh')):
            return message.channel.send("https://imgur.com/a/mq8brow")
            
    if(message.content.startswith('?mankato')):
    #        return message.channel.send("https://i.imgur.com/2B2iSkt.jpg")
            return message.channel.send(" https://media.giphy.com/media/66nOBbUf0MqbOU4DYR/giphy.gif")
    
    if(message.content.startswith('?mankatdoh')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1219042206300770354/Tech_Hockey__Minnesota_State_Highlights__031624.gif?ex=6609dc86&is=65f76786&hm=c685c71ce8200ac3d9603d19753a2d2e00706d82ac2da91345c6864c712c2e27&")
   
            
    if(message.content.startswith('?ivyleague')):
            return message.channel.send("This command has to wait another couple weeks to start playing")
            
    if(message.content.startswith('?union')):
            return message.channel.send("https://imgur.com/a/ez3Pi5Q")
            
    if(message.content.startswith('?denver')):
            return message.channel.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTNvdGZkMW1kNHU1ZHE2eWpxMXk0dmQzeXJsY2kxODd1Y2wyamoweCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/08n3hlPLRrlsBAlhfz/giphy.gif")
    if(message.content.startswith('?northeasternwins')):
            return message.channel.send("https://www.youtube.com/watch?v=RRVPTeL5udc")
            
    if(message.content.startswith('?michigantech')):
            return message.channel.send("http://www.johnsonsjerseys.net/temp/ncaa-2018.jpg")
            
    if(message.content.startswith('?nanooks')):
            return message.channel.send("https://www.youtube.com/watch?v=K9cYcRotufU")
            
    if(message.content.startswith('?spacebear')):
            return message.channel.send("https://media.giphy.com/media/Elpf1hqAotMrRTmgdY/giphy-downsized-large.gif")
            
    if(message.content.startswith('?lssu')):
            return message.channel.send("https://www.youtube.com/watch?v=HowMoUOhQSs")
            
    if(message.content.startswith('?gophers')):
            return message.channel.send("https://www.youtube.com/watch?v=X1_x1oo35L0")
    
    if(message.content.startswith('?minnesota')):
            return message.channel.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjdmMDdmMDg3YjMyMzY3YTFiZTUxYzMwNzRhZDI1NTgzYjQ4NDM0YSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/7iFEhJeCsyIqhPIs5G/giphy.gif")

    if(message.content.startswith('?miami')):
            return message.channel.send("https://www.youtube.com/watch?v=0bGpREk4Cw4")
            
    if(message.content.startswith('?dartmouth')):
            return message.channel.send("https://www.youtube.com/watch?v=Qe3iNZjenvI")
            
    if(message.content.startswith('?pennstate')):
            return message.channel.send("https://imgur.com/a/uhqlM9S")
            
    if(message.content.startswith('?rpi')):
            return message.channel.send("https://imgur.com/uAndWDQ")
            
    if(message.content.startswith('?umass') and not message.content.startswith('?umassamherst')):
            return message.channel.send("When they beat Providence tonight it will be legitimate proof that UMass deserves all of the recognition that it has received. They are 6-1 on the season and 3-0 in the conference which is an extremely impressive feat considering 2 years ago the team was not even ranked nationally.")
            
    if(message.content.startswith('?umassamherst')):
            return message.channel.send('https://cdn.discordapp.com/attachments/523161681484972062/909470794625712158/unknown.png')  
    
    if(message.content.startswith('?amherst')):
            return message.channel.send("If you are being recruited and want to play in a program that wins championships, develops you on and off the ice, invests in your long-term success and prepares you for pro hockey, there’s no better place than @UMassHockey. Believe it.")  
    if(message.content.startswith('?cornell')):
            return message.channel.send("I think you should mentally and emotionally prepare yourself that at some point Cornell University will raise two national championship banners for this lost season.\nThe students and alumni base is not going to give a shit about counter-arguments (you're welcome to declare yourselves pairwise champions) and are not going to just shrug off both the best Mens and Womens teams in several decades as a lost cause. It's going to happen, and in a few decades no one will even think it particularly controversial.")
    
    if(message.content.startswith('?maine')):
            return message.channel.send("https://i.imgur.com/4ZTkTXX.gifv")
            
    if(message.content.startswith('?newhampshire')):
            return message.channel.send("https://i.imgur.com/jWX20zw.gifv")
   
    if(message.content == '?connecticut'):
            return message.channel.send("https://imgur.com/a/cJLxgm2")
        
    if(message.content.startswith('?eng') or message.content.startswith('?emptynet')):
            return message.channel.send("https://imgur.com/a/y8w9Y1X")
            
    if(message.content.startswith('?bread')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/685911017334767840/unknown.png")        
              
    if(message.content.startswith('?bgsu') or message.content.startswith('?bowlinggreen')):
            return message.channel.send("https://media.giphy.com/media/Nv391J41hh34oL34Xr/giphy.gif")
     
    if(message.content.startswith('?hocro') or message.content.startswith('?holycross') or message.content.startswith('?hc')):
            return message.channel.send("https://media.giphy.com/media/yg3AWJeOza2XGpXRt7/giphy.gif")     
            
    if(message.content.startswith('?bemidji')):
            return message.channel.send("https://www.youtube.com/watch?v=CW_B4KB0wYs")
            
    if(message.content.startswith('?nodak')):
            return message.channel.send("https://www.youtube.com/watch?v=-B2vE1Yl2_c")
            
    if(message.content.startswith('?mtu')):
            return message.channel.send(random.choice(["https://www.youtube.com/watch?v=FZQ6VNWvmOc","https://youtu.be/6a79Ej7WK5Q?t=44"]))
    
    if(message.content.startswith('?northeastern') and not message.content.startswith('?northeasternwins')):
            return message.channel.send("https://media.giphy.com/media/jt8C9VdM1Xo6SY2Yib/giphy.gif")
            
    if(message.content.startswith('?wnortheastern')):
            return message.channel.send("https://media.giphy.com/media/008VqVNcINvZbQq7oH/giphy.mp4")       
            
    if(message.content.startswith('?rit')):
            return message.channel.send("https://j.gifs.com/q75jR0.gif")
            
    if(message.content.startswith('?almostchaos')):
            return message.channel.send("https://media.giphy.com/media/26ybwvTX4DTkwst6U/giphy.gif")
    
    if(message.content.startswith('?chaos')):
            return message.channel.send("https://tenor.com/view/chaos-gif-22919457")

    if(message.content.startswith('?russia')):
            return message.channel.send("https://media.giphy.com/media/W3keAf3qh6MwXZ8ddc/giphy.mp4")
            
    if(message.content.startswith('?wisconsin')):
            return message.channel.send("https://media.giphy.com/media/Ox6839VK0vCPTakv8H/giphy.gif")
            
    if(message.content.startswith('?brown')):
            return message.channel.send("https://media.giphy.com/media/fLtALB76zhWJULcZZn/giphy.gif")
            
    if(message.content.startswith('?colgate') or message.content.startswith('?gate')):
            return message.channel.send("https://gfycat.com/agitatedslimyhyrax")        
    if(message.content.startswith('?jdandthemouse') or message.content.startswith('?espn+')):
            return message.channel.send("https://media.discordapp.net/attachments/279689792990740481/1049856269911064627/mickeyerror.png")
    if(message.content.startswith('?portal')):
            return message.channel.send(random.choice([ "https://tenor.com/view/chosen-toy-story-gif-7936264","https://media.giphy.com/media/ciadMxfm3135m/giphy.gif"]))  
    if(message.content.startswith('?praiseportal')): 
            return message.channel.send("https://cdn.discordapp.com/attachments/900966889512128533/1108412212592259072/praiseportal.gif")
    if(message.content.startswith('?transfer') or message.content.startswith('?withthat')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1096641052259143730/ezgif.com-add-text.gif")     

    if(message.content.startswith('?hearef') or message.content.startswith('?heref')): 
        #for i in message.guild.emojis:
        #   print("<:{}:{}>".format(i.name, i.id))
        return message.channel.send('EXPERIENCE HOCKEY EAST OFFICIATING')
        
    if(message.content.startswith('?hea') and not message.content.startswith('?hearef')): 
        return message.channel.send('https://cdn.discordapp.com/attachments/523161681484972062/955960853046374410/Ex5WTvfXEAQrCkq.png')
        
    if(message.content.startswith('?lucia') or message.content.startswith('?ccharef')): 
        return message.channel.send('https://cdn.discordapp.com/attachments/523161681484972062/955134694251446302/lucia.png')    
        
    if(message.content.startswith('?spew')): 
        return message.channel.send('https://twitter.com/NUHockeyBlog/status/1505607536392773634?t=URY1TVbTxtnZrKpXay2ssQ')    
         
    if(message.content.startswith('?beanpot') and not message.content.startswith('?beanpottrot')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279688498485919744/651597256553660416/geeboston.jpg")
        
    if(message.content.startswith('?beanpottrot')):
        return message.channel.send("https://www.youtube.com/watch?v=EC2cs88XK1g")
        
    if(message.content.startswith('?beanpawt')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/761742817025327114/IMG_20201002_201354.jpg")
        
    if(message.content.startswith('?fuckharvard')):
        return message.channel.send("https://media.discordapp.net/attachments/523161681484972062/958168339576913940/8j9gyUV.jpg")
        
    #if(message.content.startswith('?bostoncollege') or message.content.startswith('?chestnuthilluniversity') or message.content.startswith('?chestnuthillcommunitycollege') or message.content.startswith('?❌oston❌ollege') or message.content.startswith('?❌hestnuthilluniversity') or message.content.startswith('?❌hestnuthill❌ommunity❌ollege')):
    if(message.content.startswith('?bostoncollege') or message.content.startswith('?chestnuthilluniversity') or message.content.startswith('?chestnuthillcommunitycollege')):
       return message.channel.send("https://media.giphy.com/media/cnEz7n3MhAIbESshGd/giphy.gif")
   
    if(message.content.startswith('?puckman')):
        return message.channel.send("https://media.discordapp.net/attachments/519719563294801922/716448834703589397/mascotmadness.png")
        
    if(message.content.startswith('?playoffot') or message.content.startswith('?playoffOT') ):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1169398545456038009/image0.jpg")    
   
    if(message.content.startswith('?merrimack')):
        return message.channel.send("https://www.youtube.com/watch?v=tU-9xtFEuk0")

    if(message.content.startswith('?mack') ):
        return message.channel.send("Is Merrimack College a respectable institution?")           

    if(message.content.startswith('?btn+')):
        return message.channel.send("There are no non-paid streams for BTN+ games available, might I suggest locating the team's radio broadcast")  
    if(message.content.startswith('?bigten')):
        return message.channel.send("https://cdn.discordapp.com/attachments/1044333097895858276/1324921765847240805/realb1gmaps.mp4")  

    if(message.content == '?slu'):
        return message.channel.send("the SLU are so fucking good")
    
    if(message.content.startswith('?huskyalliance')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/821574872290295849/image0.jpg")  
        
    if(message.content.startswith('?post')):
        return message.channel.send("PING!")
        
    if(message.content.startswith('?flagship')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/821215322823458826/image0.jpg")  
    
    if(message.content.startswith('?five-0') or message.content.startswith('?five-o')):
        return message.channel.send("https://www.youtube.com/watch?v=MC64gKvh5R8") 
        
    if(message.content.startswith('?stferrous')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/829934423310204948/StFerrous.png")
    
    if(message.content.startswith('?redsoxwin') or message.content.startswith('?dirtywater')):
        return message.channel.send("https://youtu.be/5apEctKwiD8")
    
    if(message.content.startswith('?metcalf')):
        return message.channel.send("Win your games and don’t worry about this!!")
        
    #if(message.content.startswith('?adam') or message.content.startswith('?wodon')):
    #    return message.channel.send(random.choice(["https://media.discordapp.net/attachments/279689792990740481/934507690980425758/Screenshot_20220122-125938_Twitter.jpg","https://cdn.discordapp.com/attachments/279689792990740481/1089993668582182953/image.png"]))
    
    if(message.content.startswith('?wobey')):
        return message.channel.send("https://media.discordapp.net/attachments/279689792990740481/934507690980425758/Screenshot_20220122-125938_Twitter.jpg")
    
    if(message.content.startswith('?ecac') or message.content.startswith('?ezac')):
        return message.channel.send("https://cdn.discordapp.com/attachments/498885742802632724/937154136900767764/EZAC_Hockey.png")
   
    if(message.content.startswith('?dop')):
        return message.channel.send("https://media.giphy.com/media/YhqcCh3ZHTShimyvhK/giphy.gif")
    
    if(message.content.startswith('?levi')):
        return message.channel.send("https://media.giphy.com/media/jnLhnGcoErH5bQFcJI/giphy.gif")
        
    if(message.content.startswith('?hrabal')):
        return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1220851013343248534/lolMass.gif?ex=6610711b&is=65fdfc1b&hm=f51d1e21de7f755d733c063717fdef67cc496772cc3cf74ab55bfb871562f028&")
        
    if(message.content.startswith('?mattbrown')):
        return message.channel.send("https://media.giphy.com/media/lEHjkEAz9rGgnUheLC/giphy.gif")
        
    if(message.content.startswith('?duluth')):
        return message.channel.send("https://media.giphy.com/media/pLQ3kOUCxHNbDpFNbQ/giphy.gif")
    
    if(message.content.startswith('?crasa')):
        return message.channel.send("https://media.giphy.com/media/ogRXLar48tLdC8xRLS/giphy.gif")    
        
    if(message.content.startswith('?michigan') and not message.content.startswith('?michigantech')):
            return message.channel.send("https://media.giphy.com/media/nJB57VXFHAr65qbNO1/giphy.gif")
            
    if(message.content.startswith('?goodnight') or message.content.startswith('?goodbye')):
            return message.channel.send("https://media.giphy.com/media/yoha0ouKET1h3nMaR2/giphy.gif")
        
    if(message.content.startswith('?thirdperiod')):
            #return message.channel.send("https://vxtwitter.com/sezenack/status/1723515467640307832")
            pas 
 
    if(message.content.startswith('?bentley')):
            return message.channel.send("https://cdn.discordapp.com/attachments/279689792990740481/1213925589170389052/535B4C92-B993-4C75-A4F8-FE34D794C3B2.gif?ex=65f73f4e&is=65e4ca4e&hm=c7ebd1f6a95f0dcd609405cb5cb8f2f2cc024ecff196989b75499f52262c0bf6&")
    
    if(message.content.startswith('?botson')):
            return message.channel.send("https://media.discordapp.net/attachments/530771912910176276/1175406190205878322/rendercombined.jpg?ex=656b1d51&is=6558a851&hm=7502620b8bd449188d57e33e29b24979fd1c140dcfb4a6b8a92a8692250a3717&=&width=2880&height=960")
            
    if(message.content.startswith('?botscores') or message.content.startswith('?botscore')):
        return message.channel.send("Anyone: hey Dr Bot i want a score\nBot: Sure thing! Here you go buddy!!\nAnyone: This score is wrong! You Suck!\nBot: :sob::sob::sob:")
    
    if(message.content.startswith('?stateofhockey')):
        return message.channel.send("https://media.discordapp.net/attachments/279689792990740481/1045106927316783104/unknown.png")   

    if(message.content.startswith('?redwasright')):
        return message.channel.send("```\nAll hail Red Sox Fan\nWe sing in jubilee (in jubilee)\nAll hail Red Sox Fan\nProud hater of BC (of BC)\nAll hail Red Sox Fan\nAnnoyer of JD\nThrough the years\nWe ever will proclaim\nTop mod of our hockey```") 
    if(message.content.startswith('?souza') or message.content.startswith('?extendsouza') ):
        return message.channel.send("https://cdn.discordapp.com/attachments/579830085708677120/1219466289685336184/2Q.png?ex=660b677c&is=65f8f27c&hm=fc96c1d231c8cf982d1aa67e8f035806b6b50c707e325839f7346349cbfdfade&")
        
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
    "Northeastern Huskies" : ["Northleastern", "North! Eastern! Sucks!"],
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
 