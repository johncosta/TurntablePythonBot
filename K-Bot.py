from ttapi import Bot
from pprint import pprint
from time import sleep
from collections import deque
from myConfig import *
from sys import exit
import json
import re

# There should be a file in the same directory as the bot
# that is named myConfig.py. This file shold contain some
# variables that we need to connect to tt.fm
# For example:
# myUserID      = 'XXXXXX'
# myAuthKet     = 'XXXXXX'
# defaultRoom   = 'XXXXXX'
# ownerID       = 'XXXXXX'

bot = Bot(myAuthKey, myUserID, defaultRoom)


# Todo: Enforce the DJ queue
# Command for the bot to reload the help files
# Create a class for every global variable that we have
# Change the djQueue from deque([{userid: name}]) to deque([userid]) and use the User List to get names (allows for people to change names?)
# Bel more clear with the messaging when someone does not get added to the DJ queue
# Add in a timer for the next DJ to step up. Remove any suqatters.
# Remove someone from the queue after 15 seconds of a spot opening up
# When a DJ does not step up, remove them from the queue, and annoucne the next person, if there is one
# When the next DJ has not stepped up, someone cannot add to the queue
# Pull the PM stuff back into a separate function


# Define callbacks
def roomChanged(data): 
    global theUsersList
    global theBopList
    global curSongID
    global curDjID
    global theOpList
    global maxDjCount
    global roomDJs
    roomInfo = data['room']
    roomMeta = roomInfo['metadata']
    curDjID = roomMeta['current_dj']
    songLog = roomMeta['songlog']
    curSongID = songLog[0]['_id']
    roomMods = roomMeta['moderator_id']
    maxDjCount = roomMeta['max_djs']
    #print 'curDjID: {}'.format(curDjID)
    #print 'curSongID: {}'.format(curSongID)
    #print 'roomMods: {}'.format(roomMods)

    # Reset the users list
    theUsersList = {}
    
    #Reset the bop List
    theBopList = {}

    buildRoomDjsList(roomMeta['djs'])


    #Populate the Users
    users = data['users']
    for user in users:
        theUsersList[user['userid']] = user

    #Run through the room mods. Just make every mod in the room an op
    for roomMod in roomMods:
        #print 'Checking to see if {} is an op'.format(roomMod)
        if theOpList.get(roomMod) == None:
            #print '{} is not an op. Promoting'.format(roomMod)
            theOpList[roomMod] = 0
        #else:
            #print '{} is already an op. Moving on'.format(roomMod)

    bot.modifyLaptop('linux')
    print 'The bot has changed room.'
    print 'The new room is {} and it allows {} max DJs'.format(roomInfo['name'],maxDjCount)
    print 'There are currently {} DJs'.format(roomDJs)

    if not roomDJs:
        bot.addDj()

def updateUser(data):
    print 'Update User: ',data
    
def roomInfo(data):
    global roomDJs
    global curDjID
    global curSongID
    roomInfo = data['room']
    roomMeta = roomInfo['metadata']
    curDjID = roomMeta['current_dj']
    songLog = roomMeta['songlog']
    curSongID = songLog[0]['_id']
    #roomMods = roomMeta['moderator_id']

    #Fill in the DJs
    buildRoomDjsList(roomMeta['djs'])

def speak(data):
    name = data['name']
    text = data['text']
    userID = data['userid']

    # This is a debugging line
    #print 'Debug:', data
    print '{} just said {}'.format(name, text)

    if re.match('^[!+/]',text):
        print 'Received a command: {}'.format(text[1:])
        processCommand(command=text[1:],userID=userID)

def processCommand(command,userID):
    userName = theUsersList[userID]['name']

    if command == 'hello':
        bot.speak('Hey! How are you {}?'.format(userName))

    if command == 'suck it':
        bot.speak('Whoa there. Just go ahead and settle down {}!'.format(userName))

    if command == 'user count':
        bot.speak('There are {} people jamming in here'.format(str(len(theUsersList))))

    if command == 'help':
        giveHelp(userID)

    if command == 'status':
        if theOpList.has_key(userID):
            bot.pm('You are currently an operator',userID)
        else:
            bot.pm('You, {}, are a valued member of this room'.format(userName),userID)

    if command == 'ql' or command == 'queue list':
        checkDjQueue()

    if command == 'q+' or command == 'add' or command == 'queue add':
        addToDJQueue(userID=userID,name=userName)

    if command == 'q-' or command == 'remove' or command == 'queue remove':
        removeFromDJQueue(userID=userID,name=userName)

    if command == 'theme':
        if roomTheme == None:
            bot.speak('There\'s no theme right now. Anything goes!')
        else:
            bot.speak('The theme right now is \"{}\"'.format(roomTheme))

def checkDjQueue():
    if not djQueue and len(roomDJs) < maxDjCount:
        bot.speak('There are only {} DJs! No need for a queue!'.format(len(roomDJs)))
    elif not djQueue or djQueue == None:
        bot.speak('The DJ queue is currently empty')
    else:
        queueMsg = ''
        queuePos = 0
        for dj in djQueue:
            print 'Postion {}: {}'.format(queuePos,theUsersList[djQueue[queuePos]['userID']]['name'])
            bot.speak('Q: [{}]{}'.format(queuePos+1,djQueue[queuePos]['name']))
            queuePos += 1
            sleep(0.25)
            #queueMsg += '[{}] :: {}'.format(queuePos+1,djQueue[queuePos]['name'])
            #queuePos += 1
        #bot.speak('Here is the current DJ queue: {}; '.format(queueMsg))

    
def addToDJQueue(userID, name):
    print 'Got an add request from {}, id {}'.format(name,userID)
    djInfo = {'userID':userID, 'name':name}
    print 'djInfo = {}'.format(djInfo)
    print 'We have {} DJs right now and the max is {}'.format(len(roomDJs),maxDjCount)

    print 'djQueue = {}'.format(djQueue)

    if len(roomDJs) == maxDjCount and not djInfo in djQueue and userID not in roomDJs.values(): 
        djQueue.append(djInfo)
        checkDjQueue()
        #Need to figure out the position in the deque object
        #bot.speak('Added {} to the DJ queue'.format(name))
        #print 'djQueue:', djQueue
    else:
        checkDjQueue()

def removeFromDJQueue(userID, name=None, botOp=None):
    if not name:
        name = theUsersList[userID]['name']
    djInfo = {'userID':userID, 'name':name}
    if djQueue.count(djInfo) >= 1:
        djQueue.remove(djInfo)
        if not botOp:
            bot.speak('{} has been removed from the DJ queue'.format(name))
        else:
            bot.pm('{} has been removed from the DJ queue'.format(name),botOp)
    else:
        if not botOp:
            bot.speak('{} doesn\'t seem to be in the queue'.format(name))
        else:
            bot.pm('{} is not in the queue'.format(name),botOp)

def buildRoomDjsList(djData):
    global roomDJs
    #print "We were passed a {} of DJs".format(type(djData))
    #Fill in the DJs
    if type(djData) == dict:
        roomDJs = djData
    elif type(djData) == list:
        pos = 0
        for dj in djData:
            roomDJs[str(pos)] = dj
            pos += 1


def checkIfBotShouldDJ():
    # If I am already a DJ ....
    if myUserID in roomDJs.values():
        # If there at least 2 other DJs, then I should step down
        if len(roomDJs) >= 3 and curDjID != myUserID:
            bot.remDj(myUserID)
    else:
        #If we have 0 or 1 DJs, then step up
        if len(roomDJs) <= 1 and not djQueue:
            bot.addDj()


def calculateAwesome(voteType=None, voterUid=None):
    if voteType == 'up':
        #print 'Got an upvote'
        if not theBopList.has_key(curSongID):
            theBopList[curSongID] = []
        #print theBopList
        theBopList[curSongID].append(voterUid)

    if len(theBopList[curSongID]) == (len(theUsersList))/3 and voteType == 'up':
        bot.bop()
        #bot.speak('This song is awesome')

    if len(theBopList[curSongID]) == len(theUsersList) and len(theUsersList) >= 5:
        bot.snag()
        bot.playlistAdd(curSongID)
        bot.becomeFan(curDjID)


def updateVotes(data):
    room = data['room']
    #curSongID = data['current_song']['_id']
    roomMeta = room['metadata']
    voteLog = roomMeta['votelog'][0] 
    voterUid = voteLog[0]
    voteType = voteLog[1]
    #print 'Someone has voted.',        data
    calculateAwesome(voteType, voterUid)


def registered(data):  
    global theUsersList
    user = data['user'][0]
    theUsersList[user['userid']] = user
    #print 'Someone registered.',       data
    bot.speak('Hello @{}. I\'m the WalMart greeter of this room. Type !help to see what I can do'.format(user['name']))
    if roomTheme:
        processCommand('theme',myUserID)
    calculateAwesome()
    #bot.roomInfo(roomInfo)

def deregistered(data):
    global theUsersList
    user = data['user'][0]
    del theUsersList[user['userid']]
    #print 'Someone deregistered', data
    bot.speak('Bummer that {} left.'.format(user['name']))
    calculateAwesome()
    if djQueue:
        djInfo = {'userID':user['userid'], 'name':user['name']}
        print djInfo
        if djInfo in djQueue:
            djQueue.remove(djInfo)
            print 'Removed {} from the djQueue'.format(djInfo)
        else:
            print '{} was not in the djQueue'.format(user['name'])
    else:
        print 'No djQueue'
  
def newSong(data):
    global curSongID
    global curDjID
    room = data['room']
    room_metadata = room['metadata']
    curSong = room_metadata['current_song']
    curSongID = curSong['_id']
    curDjID = curSong['djid']

    #create the bopList key
    theBopList[curSongID] = []

    bot.roomInfo(roomInfo)

    saveState()

    checkIfBotShouldDJ()

def djSteppedUp(data):
    global roomDJs
    user = data['user'][0]
    name = user['name']
    userID = user['userid']
    buildRoomDjsList(data['djs'])
    print 'DJs:', roomDJs


    # If we have a queue
    if djQueue:
        # If the new DJ was first in the queue
        if userID == djQueue[0]['userID']:
            djQueue.popleft()
            print djQueue
        else:
            bot.speak('It would appear that @{} took the DJ spot that was reserved for @{}.'.format(name, djQueue[0]['name']))

    checkIfBotShouldDJ()

def djSteppedDown(data):
    global roomDJs

    buildRoomDjsList(data['djs'])

    #If we haven't maxed out the DJ spots
    if len(roomDJs) < maxDjCount and djQueue:
        bot.speak('A DJ spot has opened up. @{} is next in line.'.format(djQueue[0]['name']))

    checkIfBotShouldDJ()

def djEscorted(data):
    global roomDJs
    escortedUser = data['user']
    escortedUserID = escortedUser['userid']
    print 'DJs:', roomDJs
    print 'a DJ was escorted offstage', data
    #roomDJs.remove(escortedUserID)
    print 'DJs:', roomDJs

    checkIfBotShouldDJ()

def endSong(data):
    print 'endsong:', roomDJs
    #userID = data['room']['metadata']['current_song']['djid']
    #name = data['room']['metadata']['current_song']['djname']
    #print 'TheUser List: {}'.format(theUsersList[roomDJs[0]])
    print 'pos 0 in the DJ queue: {}'.format(roomDJs['0'])
    if djQueue:
        bot.speak('Since we have a DJ queue, it\'s time for @{} to step down.'.format(theUsersList[roomDJs['0']]['name']))
        bot.remDj(roomDJs['0'])

    checkIfBotShouldDJ()

def noSong(data):
    checkIfBotShouldDJ()

def PlaylistToPM(data):
    print 'playlist:', data
    
def privateMessage(data):
    global curSongID
    global roomTheme
    userID = data['senderid']
    userName = theUsersList[userID]['name']
    message = data['text']
    print 'Got a PM from {}: {}'.format(userName,message)
    #print 'Current song is {}'.format(curSongID)
    #print 'room info:', bot.roomInfo()
    #bot.pm('The current song is %s' % curSongID, user)

    # If the person sending the PMs is an Op ....
    if theOpList.has_key(userID):
    #if user == '513101bbaaa5cd316ba3a24e':
        if message == 'bop':
            bot.bop()

        if message == 'snag':
            bot.pm('adding {} to my default playlist'.format(curSongID),userID)
            bot.playlistAdd(curSongID)
            bot.snag()

        if message == 'step up':
            bot.addDj()

        if message == 'skip':
            bot.skip()

        if message == 'step down':
            bot.remDj(myUserID)

        if message == 'playlist':
            bot.playlistAll(PlaylistToPM)

        if message == 'help':
            giveHelp(userID)

        if message == 'die' and userID == ownerID:
            exit()

        if re.match('^theme = ', message):
            roomTheme = message[8:]
            bot.speak('{} has set the theme for this room to \"{}\"'.format(userName,roomTheme))

        if message == 'pop':
            bot.speak('Removing {} from the queue since {} asked me to'.format(theUsersList[djQueue[0]['userID']]['name'],userName))
            djQueue.popleft()
            checkDjQueue()

        if re.match('^dq [0-9]*$',message):
            popPos = int(message[3:])-1
            dqUserId = djQueue[popPos]['userID']
            print 'Attmepting to remove {} from q{}'.format(dqUserId,popPos)
            bot.speak('Yanking {} from the queue. {} made me do it!'.format(theUsersList[dqUserId]['name'],userName))
            removeFromDJQueue(userID=dqUserId,botOp=userID)
            checkDjQueue()



    # If the person sending the PM is not an OP, then be a parrot
    else:
        bot.pm(message, userID)

def saveState():
    #json.dump(theOpList,'theOpList.json',sort_keys=True,indent=4)
    with open('theOpList.json','w') as f:
        f.write(json.dumps(theOpList,sort_keys=True,indent=4))
    with open('theBotPlaylist.json','w') as f:
        f.write(bot.playlistAll(json.dumps))

def giveHelp(userID):
    #print 'Offering some help to {}'.format(userID)
    for line in helpMsg:
        bot.pm(line.rstrip(),userID)
        sleep(0.5)
        #print line.rstrip()

    if theOpList.has_key(userID):
        for line in opHelpMsg:
            bot.pm(line.rstrip(),userID)
            sleep(0.5)
            #print line.rstrip()

def initializeVars():
    # Initialize some variables here, mostly things that we need from the get go
    global helpMsg
    global opHelpMsg
    global theOpList
    global djQueue
    global roomDJs
    global maxDjCount
    global roomTheme

    try:
        with open('theHelpFile.txt','r') as helpFile:
            helpMsg = helpFile.readlines()
    except IOError:
        print 'The file theHelpFile.txt was not found. Help may not work.'

    try:
        with open('theOpHelpFile.txt','r') as opHelpFile:
            opHelpMsg = opHelpFile.readlines()
    except IOError:
        print 'The file theOpHelpFile.txt was not found. Help may not work'

    #empty out the op list
    theOpList = {}

    #Initialize the op list
    try:
        with open('theOpList.json','r') as f:
            theOpList = json.load(f)
    except IOError:
    #if not theOpList:
        print 'Loading the default Op List'
        theOpList = {ownerID:0}
        #print 'Success'

    # Reset the users list
    theUsersList = {}
    
    #Reset the bop List
    theBopList = {}

    #Initialize the current song ID & DJ ID
    curSongID = '0'
    curDjID = '0'

    #Initialize the DJ Queue
    djQueue = deque([])
    roomDJs = {}
    maxDjCount = 1

    #Set the theme to empty
    roomTheme = None



initializeVars()

# Bind listeners
bot.on('roomChanged',   roomChanged)
bot.on('speak',         speak      )
bot.on('update_votes',  updateVotes)
bot.on('registered',    registered )
bot.on('deregistered',  deregistered)
bot.on('newsong',       newSong)
bot.on('endsong',       endSong)
bot.on('nosong',        noSong)
bot.on('pmmed',         privateMessage)
bot.on('add_dj',        djSteppedUp)
bot.on('rem_dj',        djSteppedDown)
bot.on('escort',        djEscorted)
bot.on('update_user',   updateUser)


# Start the bot
bot.start()