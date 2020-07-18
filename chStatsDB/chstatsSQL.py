import sqlite3

def generateGamesList(side1,side2,l_c_input):
    #l_c_input = int(input("1. List Games\n2. Records\n3. Both\nChoice: "))
    
    if(l_c_input==2 or l_c_input==3):
        list_count='count(*)'
        winnerStr = "SELECT {} FROM scoreData WHERE winner IN {} AND loser IN {}".format(list_count,side1,side2)
        loserStr = "SELECT {} FROM scoreData WHERE winner IN {} AND loser IN {}".format(list_count,side2,side1)
        tieStr1 = "SELECT {} FROM scoreData WHERE homeTeam IN  {} AND awayTeam IN {} AND winner = 'None'".format(list_count,side1,side2)
        tieStr2 = "SELECT {} FROM scoreData WHERE homeTeam IN  {} AND awayTeam IN {} AND winner = 'None'".format(list_count,side2,side1)
        
        c.execute(winnerStr)
        numWins = c.fetchone()[0]

        c.execute(loserStr)
        numLoses =  c.fetchone()[0]
        
        c.execute(tieStr1)
        numTies = c.fetchone()[0]
        
        c.execute(tieStr2)
        numTies += c.fetchone()[0]
        
        print("\nRecord: {}-{}-{}".format(numWins,numLoses,numTies))
        
    if(l_c_input<=1 or l_c_input>=3):
        list_count='*'
        winnerStr = "SELECT {} FROM scoreData WHERE winner IN {} AND loser IN {}".format(list_count,side1,side2)
        loserStr = "SELECT {} FROM scoreData WHERE winner IN {} AND loser IN {}".format(list_count,side2,side1)
        tieStr1 = "SELECT {} FROM scoreData WHERE homeTeam IN  {} AND awayTeam IN {} AND winner = 'None'".format(list_count,side1,side2)
        tieStr2 = "SELECT {} FROM scoreData WHERE homeTeam IN  {} AND awayTeam IN {} AND winner = 'None'".format(list_count,side2,side1)
        
        strs=[winnerStr,loserStr,tieStr1,tieStr2]
        for s in strs:
            c.execute(s)
            results= [res for res in c.fetchall()]

            for i in results:
                print(i[1],i[2],i[3],i[4])


conn = sqlite3.connect('chStats.db')
c = conn.cursor()
if __name__ == '__main__':
    c.execute("SELECT cols.name FROM pragma_table_info('teams') cols")
    colOpts= [col[0] for col in c.fetchall()]
    colDict = {}
    for i in colOpts:
        
        c.execute("SELECT {} FROM teams".format(i))
        colOpts= [col[0] for col in c.fetchall()]
        colDict[i] = list(set(colOpts))
        
    #print(colDict)

    print("Side 1")
    keyList = sorted(list(colDict.keys()));
    for i in range(len(keyList)):
        print("{}. {}".format(i+1,keyList[i]))

    choice = int(input('Select a Field: '))-1

    col1 = keyList[choice]

    print("You have chosen:",col1)  



    choiceFields = sorted(colDict[col1])
    for i in range(len(choiceFields)):
        print("{}. {}".format(i+1,choiceFields[i]))

    fieldSel = int(input('Select a Field: '))-1

    field1 = choiceFields[fieldSel]

    print("You have chosen:",field1)


    print("Side 2")
    keyList = sorted(list(colDict.keys()))
    for i in range(len(keyList)):
        print("{}. {}".format(i+1,keyList[i]))

    choice = int(input('Select a Field: '))-1

    col2 = keyList[choice]

    print("You have chosen:",col2)  



    choiceFields = sorted(colDict[col2])
    for i in range(len(choiceFields)):
        print("{}. {}".format(i+1,choiceFields[i]))

    fieldSel = int(input('Select a Field: '))-1

    field2 = choiceFields[fieldSel]

    print("You have chosen:",field2)

    side1 = "(SELECT name FROM teams where {} = '{}')".format(col1,field1)
    side2 = "(SELECT name FROM teams where {} = '{}')".format(col2,field2)

    l_c_input = int(input("1. List Games\n2. Records\n3. Both\nChoice: "))
    generateGamesList(side1,side2,l_c_input)
'''
SELECT * FROM scoreData WHERE loser IN (SELECT name FROM teams where conference = 'Hockey East') AND winner IN (SELECT name FROM teams where state = 'Minnesota');
SELECT * FROM scoreData WHERE homeTeam IN (SELECT name FROM teams where conference = 'Hockey East') AND awayTeam IN (SELECT name FROM teams where state = 'Minnesota') AND winner = 'None';
SELECT * FROM scoreData WHERE awayTeam IN (SELECT name FROM teams where conference = 'Hockey East') AND homeTeam IN (SELECT name FROM teams where state = 'Minnesota') AND winner = 'None';
'''
    
    

