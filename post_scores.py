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
    
updateTime =  datetime.now()
updateTime = updateTime.strftime("%Y-%m-%d %H:%M:%S ET")

for submission in subreddit.hot(limit=10):
    if(submission.title.find("[Game Thread]")>=0 and (scoreDate in submission.title or ("Week of" in submission.title and isTodayScores))):
        scoreboard += "\n\nLast Updated: " + str(updateTime)
        isFound = False
        for comment in submission.comments:
            if(comment.author== 'ch_scorebot'):
                   isFound=True
                   comment.edit(scoreboard)
        if(not isFound):
            submission.reply(scoreboard)


