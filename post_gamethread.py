import praw
import os
import pytz
from datetime import datetime,date
import calendar
import scorebot

reddit = praw.Reddit("bot1")
reddit.validate_on_submit = True
subreddit = reddit.subreddit('collegehockey')

def ordinaltg(n):
  return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")
  
  
est = pytz.timezone('US/Eastern')
DOW=calendar.day_name[date.today().weekday()]
try:
    scoreboard  = scorebot.generateScoreboard()
except:
    exit()
    
if(scorebot.gameDate  == ''):
    exit()
    
scoreDate = scorebot.gameDate


sDate = scoreDate.split(',')
day = sDate[0]
altDate = sDate[1]+" "+sDate[2];
isTodayScores = False
if(day == calendar.day_name[date.today().weekday()]):
    isTodayScores=True
    
else:
    exit()

if(scoreboard == ""):
    exit()
 
updateTime =  datetime.now()
updateTime = updateTime.strftime("%Y-%m-%d %H:%M:%S ET")
#dateString="{}, {} {} {}".format(day,sDate[1],ordinaltg(date.today().day),date.today().year)
dateString =  scorebot.gameDate
# https://www.youtube.com/watch?v=QvmJxKbgxr8
# https://www.youtube.com/watch?v=o0YWRXJsMyM
header = '''
IT'S GAMEDAY!

Grab your gear, crack some beers, and get ready to cheer!  [LET'S GO COLLEGE HOCKEY!]({})

***
***
##[FLAIR UP HERE!](https://www.reddit.com/r/collegehockey/wiki/flair)

## Live Scores Bot (ME!)
Built by /u/redsoxfan2194 

##[Comment Reporting Guidelines](https://www.reddit.com/r/collegehockey/comments/9ih43r/reporting_commentsposts/)

##[The /r/collegehockey Discord server!](https://discord.gg/rvX5kb8)

Brought to you by /u/LocksTheFox


***
***
'''

footer='''
***
***
#Quick links for streaming only/locally televised games

Service | Home Team/Conferences
---|---
[B1G+](https://www.bigtenplus.com/) ($$$) | [Big Ten](#f/bigten), [Penn State](#f/pennstate) women, [WCHA](#f/wcha)
[Cuse TV](https://cuse.com/watch/) | [Syracuse](#f/syracuse)
[ESPN+](https://www.espn.com/espnplus/?om-navmethod=topnav)^1 ($$$) | [ECAC](#f/ecachockey) , [Hockey East](#f/hockeyeast)
[FloHockey](https://www.flohockey.tv/) ($$$) | [Atlantic Hockey](#f/atlantichockey), [Alaska](#f/alaskafairbanks), [CCHA](#f/ccha), [Lindenwood](#f/lindenwood) women, [Mercyhurst](#f/mercyhurst) women, [RIT](#f/rit) women  
[NEC Front Row](http://necfrontrow.com/schools/LIU) | [Long Island](#f/liu),  [Sacred Heart](#f/sacredheart) women, [Stonehil](#f/stonehill)
[NE-10 Now](https://portal.stretchinternet.com/ne10/) | [Franklin Pierce](#f/franklinpierce), [St Anselm](#f/stanselm), [Saint Michael's](#f/stmichaels)
[NCHC.tv](https://www.nchc.tv) ($$$) | [NCHC](#f/nchc)
[Pac12 Live Stream](https://pac-12.com/sports/schedule)^2 | [Arizona State](#f/arizonastate)
[YouTube](https://www.youtube.com/channel/UC0tjLDGhQlMriBVz8egKu_A) | [Anchorage](#f/alaskaanchorage) 

1: US Only links for [ECAC](https://www.espn.com/watch/catalog/2c1e3eb6-667b-4e95-8820-c594ee8c7f52/ecac-hockey#bucketId=29784&sourceCollection=Browse_By_Top_Conferences), [Hockey East] (https://www.espn.com/watch/catalog/56a061bd-b214-4ed2-a63e-1fa71a59c9f3/hockey-east#bucketId=29784&sourceCollection=Browse_By_Top_Conferences), International links for [Ivy](https://portal.stretchinternet.com/ivy/), [Rest of ECAC](https://portal.stretchinternet.com/ecachockey/), [Hockey East](https://portal.stretchinternet.com/hockeyeast/)  
2: ASU games stream on Pac12 Insider or the ASU Live Stream channels, both are free to access

***
**Discuss whatever you wish.  You can trash talk, but please keep it civil!**

**Turning comment sort to 'new' will help you see the newest posts.**
'''
text=''
est = pytz.timezone('US/Eastern')
title = '[Game Thread] {}{}'.format(dateString,text)
scoreboard += "\n\nLast Updated: " + str(updateTime) 
upGTVideoPath = '/home/nmemme/ch_scorebot/titles/upcomingGTvideo.txt'
currGTVideoPath = '/home/nmemme/ch_scorebot/titles/currentGTvideo.txt'
if(os.path.exists(upGTVideoPath)):
    file=open(upGTVideoPath,'r')
    vid = file.readline()
    vid = vid.rstrip('\n')
    file.close()
    os.remove(upGTVideoPath)
    file2=open(currGTVideoPath,'w')
    file2.write(vid)
    file2.close()
elif(os.path.exists(currGTVideoPath)):
    file=open(currGTVideoPath,'r')
    vid = file.readline()
    vid=vid.rstrip('\n')
else:
    vid="https://www.youtube.com/watch?v=o0YWRXJsMyM"
    
bodScore = header.format(vid) + scoreboard + footer
try:
    for submission in subreddit.hot(limit=20):
      if(submission.title.find("[Game Thread] "+day)>=0 and submission.title.find(day)>=0):
        daysSince = (est.localize(datetime.now())-est.localize(datetime.fromtimestamp(int(submission.created_utc)))).days
        if(daysSince>=6):
            upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTTitle.txt'
            currGTFilePath = '/home/nmemme/ch_scorebot/titles/currentGTTitle.txt'
            if(os.path.exists(upGTFilePath)):
                file=open(upGTFilePath,'r')
                text = file.readline()
                text=text.rstrip('\n')
                file.close()
                os.remove(upGTFilePath)
                file2=open(currGTFilePath,'w')
                file2.write(text)
                file2.close()
                text=' - ' + text
            title = '[Game Thread] {}{}'.format(dateString,text)
            subreddit.submit(title,selftext=bodScore,send_replies=False)
            exit()
        else:
            if(submission.title.find("[Game Thread] " + day)>=0 and submission.author== 'ch_scorebot'):
                submission.edit(body=bodScore) 
                exit()  

    if(isTodayScores): 
        upGTFilePath = '/home/nmemme/ch_scorebot/titles/upcomingGTTitle.txt'
        currGTFilePath = '/home/nmemme/ch_scorebot/titles/currentGTTitle.txt'
        if(os.path.exists(upGTFilePath)):
            file=open(upGTFilePath,'r')
            text = file.readline()
            text=text.rstrip('\n')
            file.close()
            os.remove(upGTFilePath)
            file2=open(currGTFilePath,'w')
            file2.write(text)
            file2.close()
            text=' - ' + text
            title = '[Game Thread] {}{}'.format(dateString,text)
        subreddit.submit(title,selftext=bodScore,send_replies=False)
        exit()

except:
    pass
