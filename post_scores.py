import scorebot
import praw
import os
from datetime import datetime,date
import calendar
reddit = praw.Reddit("bot1")
reddit.validate_on_submit = True
subreddit = reddit.subreddit('collegehockey')
scoreboard  = scorebot.generateScoreboard()
if(scorebot.gameDate  == ''):
    exit()
scoreDate = scorebot.gameDate
sDate = scoreDate.split(' ')
day = sDate[0]
altDate = sDate[1]+" "+sDate[2];
isTodayScores = False
if(day == calendar.day_name[date.today().weekday()]):
    isTodayScores=True

if(scoreboard == ""):
    exit()
updateTime =  datetime.now()
updateTime = updateTime.strftime("%Y-%m-%d %H:%M:%S ET")

for submission in subreddit.hot(limit=20):
    if(submission.title.find("[Game Thread]")>=0 and ((submission.title.find(day)>=0) or ("Week of" in submission.title and isTodayScores))):
        
        scoreboard = "##" + day + "'s Scores: \n" + scoreboard
        scoreboard += "\n\nLast Updated: " + str(updateTime)
        if(submission.title.find("Week of")>=0 and (day == "Saturday" or day == "Friday")):
            #exit()
            pass
        for comment in submission.comments:
            if(comment.author== 'ch_scorebot'):
                #if("Week of" in submission.title and isTodayScores and (day != "Saturday") and (day != "Friday")):
                if("Week of" in submission.title and isTodayScores):
                    if(day in comment.body):
                           comment.edit(scoreboard)
                           exit()
                    for r in comment.replies:
                       if(r.author == 'ch_scorebot' and day in r.body):
                           r.edit(scoreboard)
                           exit()
                    comment.reply(scoreboard)
                    exit()
                elif(day in submission.title):
                   comment.edit(scoreboard)
                   exit()
                else:
                   exit()
        submission.reply(scoreboard)
        exit()
