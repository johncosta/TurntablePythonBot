import time

from ttapi import Bot

from ttpbot import utils
from ttresponse import User, Room


class TTpBot(Bot):

    operators = []
    users = {}
    bop_list = {}
    room_djs = []

    def __init__(self, *args, **kwargs):
        """ Initializes the Bot

        :param auth_key: Authorization key, specific to your user
        :param user_id: Turntable.fm id for the bot
        :param room_id: Initial Turntable.fm room id for the bot
        :param ownerID: Owner id of the bot. this is your non-bot Turntable.fm
        id
        """
        self.owner_id = kwargs.pop('owner_id', None)
        super(TTpBot, self).__init__(*args, **kwargs)

        # This seems like a bug in the api. Speak requires
        # roomID to be set but init requires room_id
        self.roomId = kwargs.pop('room_id', None)

        self.logger = utils.configure_logger(self.__class__)

        self.bot_id = args[1]
        self.operators.append(self.owner_id) if self.owner_id else None

        self.on('roomChanged', self.room_changed)
        self.on('registered', self.registered)
        self.on('deregistered', self.deregistered)
        self.on('speak', self.parrot)
        self.on('newsong', self.new_song)
        self.on('endsong', self.end_song)
        self.on('nosong', self.no_song)
        self.on('add_dj', self.dj_stepped_up)
        self.on('rem_dj', self.dj_stepped_down)

        self.commands = self._build_commands()

        # self.on('update_votes',  updateVotes)
        # self.on('pmmed',         privateMessage)
        # self.on('add_dj',        djSteppedUp)
        # self.on('rem_dj',        djSteppedDown)
        # self.on('escort',        djEscorted)
        # self.on('update_user',   updateUser)
        # self.on('snagged',       songSnagged)
        # self.on('new_moderator', newModerator)
        # self.on('rem_moderator', remModerator)

        # TODO initialize database

    def _build_commands(self):
        """ Builds the command list. There are two types of commands.

                1) Parrot commands - users can say text and the bot will
                    speak some usually, witty command
                2) Operator command - this executes some sort of logic
                    that executes an method, usually some sort of
                    queue management operation
        """
        pass
        #self._load("help.txt")
        #self.op_message = self._load("op.txt")

    def _load(self, file_name, file_lines=None):
        try:
            with open(file_name,'r') as file_contents:
                file_lines = file_contents.readlines()
        except IOError:
            self.logger.error(
                "The file %s was not found. Help may not work.".format(
                file_name))
        return file_lines

    def _roomInfo(self, data):

        self.logger.debug("In room info")
        room = Room(data.get('room'))
        #self.logger.debug("Room Data: {0}".format(room.__dict__))

        self.room_djs = room.djs
        self.logger.debug("Room djs: {0}".format(room.djs))

        self.current_dj = room.current_dj
        self.logger.debug("Current DJ: {0}".format(room.current_dj))

    def _bot_should_dj(self, bot_id, dj_ids):
        """ Only dj if there's less than 2 people in the room

        :param bot_id: id of this bot
        :param dj_ids: list of current djs
        """
        if len(dj_ids) == 0:
            return self.addDj()

        if len(dj_ids) == 1 and bot_id not in dj_ids:
            return self.addDj()

        if len(dj_ids) > 2 and bot_id in dj_ids:
            return self.remDj(bot_id)

    def talk(self, msg):
        """ Wrapper for speak, encapsulates the time delay """
        time.sleep(1)
        self.speak(msg)

    def registered(self, data):
        """ Registered seems to occur when a user enters the room.  This could
        be the bot itself or another user.
        """
        self.logger.debug("Enter registered")
        self.logger.debug("Data: {0}".format(data))
        user = User(data.get('user')[0])

        self.logger.debug("Adding user ({0})".format(user.name))
        self.users.update({user.userid: user})

        msg = 'Hello {0}. Type !help to see what I can do'.format(user.name)
        self.talk(msg)

    def deregistered(self, data):
        """ Deregistered seems to occur when a user exists the room.  This
        could be the bot itself or another user.
        """
        self.logger.debug("Enter deregistered")
        self.logger.debug("Data: {0}".format(data))
        user = User(data.get('user')[0])

        self.logger.debug("Removing user ({0})".format(user.userid))
        self.users.pop(user.user_id, None)

    def parrot(self, data):
        """ When someone speaks in the channel, this handler is used to capture
        and parse the output looking for bot commands. We don't want to shadow
        the bot method `speak` so the alternate method name `parrot` is used.
        """
        name = data['name']
        text = data['text']
        user_id = data['userid']

        self.logger.debug('{0} just said \"{1}\"'.format(name, text))

    def room_changed(self, data):
        """ information about the room
        """
        self.logger.debug("In room changed")
        room = Room(data.get('room'))
        #self.logger.debug("Room Data: {0}".format(room.__dict__))

        self.room_djs = room.djs
        self.logger.debug("Room djs: {0}".format(room.djs))

        self.users = {}
        user_list = [User(user) for user in data.get('users')]
        for user in user_list:
            self.users.update({user.userid: user})
        self.logger.debug("Room users: {0}".format(self.users))

        self._bot_should_dj(self.bot_id, self.room_djs)
        #
        # buildOpList(roomMods)
        #
        # bot.modifyLaptop('linux')
        # #print 'The bot has changed room.'
        # #print 'The new room is {} and it allows {} max DJs'.format(roomInfo['name'],maxDjCount)
        # #print 'There are currently {} DJs'.format(roomDJs)
        #
        # self.adjust_my_dj_status()

    def new_song(self, data):
        """ Handler for new songs
        """
        self.roomInfo(self._room_info)
        self._bot_should_dj(self.bot_id, self.room_djs)

    def end_song(self, data):
        """ handler for end of songs
        """
        self.roomInfo(self._room_info)
        self._bot_should_dj(self.bot_id, self.room_djs)

    def no_song(self, data):
        """ handler for no songs
        """
        self.roomInfo(self._room_info)
        self._bot_should_dj(self.bot_id, self.room_djs)

    def dj_stepped_up(self, data):
        """ Handler for when a dj steps up
        """
        self.room_djs = [v for k, v  in data.get('djs', None).iteritems()]
        self.logger.debug("Room djs: {0}".format(self.room_djs))
        self._bot_should_dj(self.bot_id, self.room_djs)

    def dj_stepped_down(self, data):
        """ Handler for when a dj steps down
        """
        self.room_djs = [v for k, v  in data.get('djs', None).iteritems()]
        self.logger.debug("Room djs: {0}".format(self.room_djs))
        self._bot_should_dj(self.bot_id, self.room_djs)
