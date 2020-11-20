import praw
import os
import pytz
from datetime import datetime,date
import calendar
reddit = praw.Reddit("bot1")
reddit.validate_on_submit = True
subreddit = reddit.subreddit('collegehockey')
est = pytz.timezone('US/Eastern')
DOW=calendar.day_name[date.today().weekday()]

def getTrashTitle():
    comment='SOMEONE FORGOT TO MAKE A WITTY TITLE'
    upTrashFilePath = '/home/nmemme/ch_scorebot/titles/upcomingTrashTitle.txt'
    currTrashFilePath = '/home/nmemme/ch_scorebot/titles/currentTrashTitle.txt'
    if(os.path.exists(upTrashFilePath)):
        file=open(upTrashFilePath,'r')
        comment = file.readline()
        comment=comment.rstrip('\n')
        file.close()
        os.remove(upTrashFilePath)
        file2=open(currTrashFilePath,'w')
        file2.write(comment)
        file2.close()
    
    return comment
                
if DOW=='Sunday':
    title='Sidebar Submission Sunday'
    text='''Please submit your pic for the sidebar this week.

Standard size is 300x300px

Please do not downvote posts based on fandom

Keep it civil, don't be a jerk

Thread closes on Tuesday morning

Most popular pic will be the sidebar for the week (pending mod approval)
'''


elif DOW=='Monday':
    exit()
    
elif DOW=='Tuesday':
    exit()
    
elif DOW=='Wednesday':
    exit()
    
elif DOW=='Thursday':
    title='TRASH TALK THURSDAY'
    text = '''
ITS MIDNIGHT, ITS THURSDAY, AND THAT MEANS ONE THING...IT IS TIME FOR SOME TRASH TALK!


**RULES**


**[FLAIR UP!](https://www.reddit.com/r/collegehockey/wiki/flair)**


**CAPS LOCK ON! (WITH THE EXCEPTION BEING USERNAME SHOUT OUTS! E.G, /u/Whoa_throwaway IS A SIEVE!) [SEE THE DRAWING IF YOU FAIL TO UNDERSTAND THIS COMPLEX PROCESS OR *INSERT WHATEVER YOU WANT HERE*](https://i.imgur.com/r1hi49B.jpg)**


**IF YOU WOULDN'T SAY IT AT A GAME DON'T POST IT HERE!**'''

    
elif DOW=='Friday':
    title="Free Talk Friday"
    text='sup'
    
    
elif DOW=='Saturday':
    exit()
     
for submission in subreddit.hot(limit=20):
  if(submission.title.find(title)>=0):
    daysSince = (datetime.now().astimezone(est)-datetime.fromtimestamp(int(submission.created_utc)).astimezone(est)).days
    if(daysSince>=6):
        if(title=='TRASH TALK THURSDAY'):
            title = 'TRASH TALK THURSDAY: "{}" EDITION'.format(getTrashTitle())
        subreddit.submit(title,text,send_replies=False)
        exit()
    else:
        exit() 
if(title=='TRASH TALK THURSDAY'):
    title = 'TRASH TALK THURSDAY: "{}" EDITION'.format(getTrashTitle())
subreddit.submit(title,text,send_replies=False)
exit()
