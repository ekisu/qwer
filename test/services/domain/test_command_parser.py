from qwer.services.domain.command_parser import CommandParser
from qwer.domain.value_objects.command_invocation import CommandInvocation
import unittest


class TestCommandParser(unittest.TestCase):
    command_parser: CommandParser

    def setUp(self) -> None:
        self.command_parser = CommandParser()

    def test_parse_should_be_None_when_message_is_not_a_command(self):
        message_contents = 'normal message'

        invocation = self.command_parser.parse(message_contents)

        self.assertIsNone(invocation)

    def test_parse_should_parse_command_without_arguments_correctly(self):
        message_contents = '!test_command'
        expected_invocation = CommandInvocation(
            command_name='test_command',
            command_arguments=[]
        )

        invocation = self.command_parser.parse(message_contents)

        self.assertEqual(invocation, expected_invocation)

    def test_parse_should_parse_command_with_arguments_correctly(self):
        message_contents = '!test_command argument1 argument2'
        expected_invocation = CommandInvocation(
            command_name='test_command',
            command_arguments=['argument1', 'argument2']
        )

        invocation = self.command_parser.parse(message_contents)

        self.assertEqual(invocation, expected_invocation)
