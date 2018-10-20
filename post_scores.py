import scorebot
import praw
import os
from datetime import datetime,date
import calendar
reddit = praw.Reddit("bot1")
subreddit = reddit.subreddit('collegehockey')
scoreboard  = scorebot.generateScoreboard()
scoreDate = scorebot.gameDate
sDate = scoreDate.split(' ')
day = sDate[0]
isTodayScores = False
if(day == calendar.day_name[date.today().weekday()]):
    isTodayScores=True

if(scoreboard == ""):
    exit()
updateTime =  datetime.now()
updateTime = updateTime.strftime("%Y-%m-%d %H:%M:%S ET")

for submission in subreddit.hot(limit=20):
    if(submission.title.find("[Game Thread]")>=0 and day in submission.title or ("Week of" in submission.title and isTodayScores)):
        scoreboard = "##" + day + "'s Scores: \n" + scoreboard
        scoreboard += "\n\nLast Updated: " + str(updateTime)
        isFound = False
        
        for comment in submission.comments:
            if(comment.author== 'ch_scorebot'):
                hasReply = False
                if("Week of" in submission.title and isTodayScores):
                    for r in comment.replies:
                       if(r.author == 'ch_scorebot' and day in r.body):
                           r.edit(scoreboard)
                           exit()
     
                    comment.reply(scoreboard)
                    exit()
                elif(scoreDate in submission.title):
                   comment.edit(scoreboard)
                   exit()
                
        submission.reply(scoreboard)
        exit()
