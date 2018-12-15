import scorebot
import discord

TOKEN = 'NTIzMTYxNzgyNjY4MjMwNjU3.DvVgTQ.qFkGJSxmC3jqEgX15khYBiC8lkQ'
    #scorebot.getScores()
    #games=scorebot.gameList
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('?score '):
        team = decodeTeam(message.content.split('?score ')[1])
        msg = generateScoreline(team, "Men")
        if(len(msg)>0):
            await client.send_message(message.channel, msg)
            
    if message.content.startswith('?mscore '):
        team = decodeTeam(message.content.split('?mscore ')[1])
        msg = generateScoreline(team, "Men")
        if(len(msg)>0):
            await client.send_message(message.channel, msg)
       
            
    if message.content.startswith('?wscore '):
        team = decodeTeam(message.content.split('?wscore ')[1])
        msg = generateScoreline(team, "Women")
        if(len(msg)>0):
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def decodeTeam(team):
    team=team.lower()
    team=team.replace(" ","")
    team=team.replace("-","")
    team=team.replace("'","")
    dict={"afa" : "Air Force",
        "aic" : "American International",
        "aic" : "AmericanInternational",
        "alabamahuntsville" : "Alabama Huntsville",
        "americanintl" : "American International",
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
        "hc" : "Holy Cross",
        "howlinhuskies" : "Northeastern",
        "huntsville" : "Alabama Huntsville",
        "keggy" : "Dartmouth",
        "lakestate" : "Lake Superior State",
        "lakesuperior" : "Lake Superior State",
        "lowell" : "UMass Lowell",
        "lssu" : "Lake Superior State",
        "lu" : "Lindenwood",
        "mack" : "Merrimack",
        "mankato" : "Minnesota State",
        "mc" : "Merrimack",
        "mich" : "Michigan",
        "mnsu" : "Minnesota State",
        "mrbee" : "American International",
        "msu" : "Michigan State",
        "mtu" : "Michigan Tech",
        "nd" : "Notre Dame",
        "nebraskaomaha" : "Omaha",
        "neu" : "Northeastern",
        "newtonsundayschool" : "Boston College",
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
        "smc" : "Saint Michael's",
        "sparky" : "Arizona State",
        "sparty" : "Michigan State",
        "stanselm" : "Saint Anselm",
        "stcloud" : "St. Cloud State",
        "stmichaels" : "Saint Michael's",
        "stmikes" : "Saint Michael's",
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
        "wmu" : "Western Michigan",
        "ziggy" : "Bowling Green"}

    if team in dict:
        return dict[team]
    else:
        teamName=''
        teamSplit = team.split(' ')
        for i in range(len(teamSplit)):
            teamName+=teamSplit[i].capitalize()
            if(i<len(teamSplit)-1):
                teamName+=' '
        return teamName
def generateScoreline(team, m_w):
    scorebot.getScores()
    games=scorebot.gameList
    if scorebot.isD1(team,team,m_w):
        for game in games:
            if(game['homeTeam'] == team or game['awayTeam'] == team and game['m_w']==m_w):
                return "{} {}\n{} {}\n{}".format(game['awayTeam'],game['awayScore'],game['homeTeam'],game['homeScore'],game['status'])
        return "No game scheduled for {} {}".format(team,m_w)
    return ":regional_indicator_x: Team Not Found"
client.run(TOKEN)