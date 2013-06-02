import unittest

from ttpbot.commands.command import BotCommands, TextCommand


class CommandFixture(unittest.TestCase):

    def setUp(self):
        self.commands = BotCommands()

    def test(self):
        result = self.commands.interpret("!hello")
        self.assertIsNotNone(result)
        self.assertEqual(result.key, "hello")

