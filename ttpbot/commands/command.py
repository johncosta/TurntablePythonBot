class TextCommand(object):
    """ Text commands have a key and a value.  The value may have an optional
        set of arguments
    """
    def __init__(self, key, value, args):
        self.key = key
        self.value = value
        self.args = args


class OperationCommand(object):

    def execute(self):
        pass


class BotCommands(dict):
    """ Dictionary of the commands.  There are two types of commands.

        1) Text commands - users can say text and the bot will
            speak some usually, witty command

        2) Operator command - this executes some sort of logic
            that executes an method, usually some sort of
            queue management operation, it may optionally have the
            bot speak a command

    """
    DEFAULT_COMMAND_PREFIX = "!"

    def __init__(self):
        # TODO take a file of some sort to build up
        #  the set of interactive commands
        """
        :param bot: the bot which has the commands to execute
        """
        self.clear()
        self.update({'hello': TextCommand("hello", "Hi, {name}!", ('user',))})

    def _find_command(self, word, commands, command_prefix, command=None):
        # TODO non prefixed commands
        if word.startswith(command_prefix):
            command = commands.get(word[1:], None)
        return command

    def _parse(self, msg, commands, command_prefix, command=None):
        if msg and isinstance(msg, basestring):
            for word in msg.split(' '):
                command = self._find_command(word, commands, command_prefix)
        return command

    def interpret(self, msg, command=None):
        """ Looks for a command and returns it if one is found
        """
        # parse for a command
        command = self._parse(msg, self, self.DEFAULT_COMMAND_PREFIX)
        return command

