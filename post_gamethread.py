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

Home Team/Conference | Service
---|---
[Atlantic Hockey](#f/atlantichockey), [Alaska](#f/alaskafairbanks), [CCHA](#f/ccha) | [FloHockey](https://www.flohockey.tv/) ($$$)
[Big Ten](#f/bigten), [Penn State](#f/pennstate) women, [WCHA](#f/wcha) | [B1G+](https://www.bigtenplus.com/) ($$$)
[ECAC](#f/ecachockey) | [ESPN+](https://www.espn.com/espnplus/?om-navmethod=topnav)^1 ($$$), [Ivy International Stream](https://portal.stretchinternet.com/ivy/)^2 ($$$), [ECAC International Stream](https://portal.stretchinternet.com/ecachockey/)^2 ($$$), [RPItv](http://rpitv.org/)^3
[Hockey East](#f/hockeyeast) | [SportsLive](https://www.collegesportslive.com/hockeyeast/)^4, [Hockey East on NESN](https://www.collegesportslive.com/NESN/)^4
[NCHC](#f/nchc) | [NCHC.tv](https://www.nchc.tv)^4 ($$$)
[Arizona State](#f/arizonastate) | [ASU Live Stream](https://pac-12.com/live/arizona-state-university)^5, [Pac12 Insider](https://pac-12.com/live?networks=P12I) 
[Franklin Pierce](#f/franklinpierce), [St Anselm](#f/stanselm), [Saint Michael's](#f/stmichaels) | [NE-10 Now](https://portal.stretchinternet.com/ne10/)
[Lindenwood](#f/lindenwood), [Mercyhurst](#f/mercyhurst) women, [RIT](#f/rit) women  | [CHA Digitial Network](https://portal.stretchinternet.com/cha/) ($$$)
[Long Island](#f/liu) | [NEC Front Row](http://necfrontrow.com/schools/LIU)
[Post](#f/post) | [CACC Network](https://www.caccnetwork.com/post/)
[Sacred Heart](#f/sacredheart) women | N/A^6
[Syracuse](#f/syracuse) | [Cuse TV](https://cuse.com/watch/)


1: US Only  
2: International only; ECAC International does not include the Ivies or RPI  
3: Currently simulcasting on ESPN+, possible future geoblocking unknown  
4: Select HEA and NCHC games also available on the CBS Sports App; HEA on NESN games blacked out in New England on all ViacomCBS services  
5: Link to main live stream; ASU maintains separate pages for additional streams in the event of multiple simultaneous sports being streamed  
6: Sacred Heart opts not to air any home women's contests

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
