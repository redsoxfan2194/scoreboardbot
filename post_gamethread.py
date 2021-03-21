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
sDate = scoreDate.split(' ')
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
dateString="{}, {} {} {}".format(day,sDate[1],ordinaltg(date.today().day),date.today().year)


header = '''
IT'S GAMEDAY!

Grab your gear, crack some beers, and get ready to cheer!  [LET'S GO COLLEGE HOCKEY!](https://www.youtube.com/watch?v=o0YWRXJsMyM)

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
#Streaming Quick Links

Home team determines the rights to the telecast

|TV Network Streams^1 | Paid Streams^2 | Free Streams^2
|:-:|:-:|:-:|
[Altitude Now](https://www.altitudenow.com/) | [BTN+](https://www.btnplus.com/) | [CACC Network](http://caccnetwork.com/post/)
[AT&T SportsNet Rocky Mountain](https://rockymountain-attsn.att.com/)  | [CHA Digital Network](https://portal.stretchinternet.com/cha/)| [Cuse TV](https://cuse.com/watch)
[CBSSN](http://www.cbssports.com/cbs-sports-network/) | [ESPN+](http://www.espn.com/watch/espnplus)  | [NE-10 Now](https://portal.stretchinternet.com/ne10/) 
[Fox Sports](https://www.foxsports.com/live)^3 | [FloHockey.tv](https://www.flohockey.tv/)  | [NEC Front Row](http://necfrontrow.com/schools.php?title=LIU) 
[Fox Sports Go](https://www.foxsportsgo.com/)^4 | [NCHC.tv](https://www.nchc.tv/)  | [Pac-12 Live Stream](https://pac-12.com/sports/schedule/network/live-stream/)
[NBC Sports](https://www.nbcsports.com/live) | [TSN Direct](https://www.tsn.ca/live)^5  | [RPItv YouTube Page](https://www.youtube.com/user/RPITV)
[NESNGo](https://nesngo.nesn.com/) | | [College Sports Live] (https://www.collegesportslive.com/hockeyeast/)^6 |
[WatchESPN](http://www.espn.com/watch/?categoryId=25) |  |


1: Requires Authenticated Login  
2: Potentially Subject to blackout if televised in your area    
3: Games on FS1/FS2/BTN  
4: Games on Fox Sports Regionals (Rebrand following sale to Sinclair pending)  
5: Available as direct subscription or with TSN cable subscription (CA only) 

6: Non-NESN games, games on NESN are found [here](https://www.collegesportslive.com/NESN/) (blacked out in NESN's tv territory, or at least in theory)

***
***

##Shamelessly stolen from /r/hockey's GDT notes:

* Discuss whatever you wish.  You can trash talk, but please keep it civil!
* Turning comment sort to 'new' will help you see the newest posts.
* Try [Chrome Refresh](https://chrome.google.com/webstore/detail/chrome-refresh/aifhnlnghddfdaccgbbpbhjfkmncekmn) or [Firefox ReloadEvery](http://reloadevery.mozdev.org/)
'''
text=''
est = pytz.timezone('US/Eastern')
title = '[Game Thread] {}{}'.format(dateString,text)
scoreboard += "\n\nLast Updated: " + str(updateTime)      
body = header + scoreboard + footer

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
            subreddit.submit(title,body,send_replies=False)
            exit()
        else:
            if(submission.title.find("[Game Thread] " + day)>=0 and submission.author== 'ch_scorebot'):
                submission.edit(body) 
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
        subreddit.submit(title,body,send_replies=False)
        exit()

except:
    pass
