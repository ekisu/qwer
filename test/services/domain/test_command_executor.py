from qwer.services.domain.command_executor import CommandExecutor
from qwer.domain.value_objects.command_invocation import CommandInvocation
from qwer.domain.entities.command import Command
import unittest

class TestCommandExecutor(unittest.TestCase):
    command_executor: CommandExecutor

    def setUp(self) -> None:
        self.command_executor = CommandExecutor()

    def build_command(self, contents: str, name: str = 'test_command') -> Command:
        return Command(
            guild_id=123,
            name=name,
            contents=contents
        )

    def test_execute_should_return_contents_when_command_has_no_calls(self):
        simple_command = self.build_command('Hello, World!')

        invocation = CommandInvocation('test_command', [])

        result = self.command_executor.execute(simple_command, invocation)

        self.assertEqual(result, simple_command.contents)
    
    def test_execute_should_replace_arguments_when_contents_use_arguments(self):
        command_with_template = self.build_command('Hello, {{invocation.command_arguments[0]}}!')

        invocation = CommandInvocation('test_command', ['Yuko'])

        expected_result = 'Hello, Yuko!'
        result = self.command_executor.execute(command_with_template, invocation)

        self.assertEqual(result, expected_result)
