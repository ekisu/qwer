from qwer.services.domain.command_functions import AbstractCommandFunctions
from unittest.mock import Mock, create_autospec
from qwer.services.domain.command_executor import CommandExecutor
from qwer.domain.value_objects.command_invocation import CommandInvocation
from qwer.domain.entities.command import Command
import unittest

class TestCommandExecutor(unittest.IsolatedAsyncioTestCase):
    command_executor: CommandExecutor

    def setUp(self) -> None:
        self.command_executor = CommandExecutor()

    def build_command(self, contents: str, name: str = 'test_command') -> Command:
        return Command(
            guild_id=123,
            name=name,
            contents=contents
        )

    async def test_execute_should_return_contents_when_command_has_no_calls(self):
        simple_command = self.build_command('Hello, World!')

        invocation = CommandInvocation('test_command', [])

        result = await self.command_executor.execute(simple_command, invocation)

        self.assertEqual(result, simple_command.contents)
    
    async def test_execute_should_replace_arguments_when_contents_use_arguments(self):
        command_with_template = self.build_command('Hello, {{invocation.command_arguments[0]}}!')

        invocation = CommandInvocation('test_command', ['Yuko'])

        expected_result = 'Hello, Yuko!'
        result = await self.command_executor.execute(command_with_template, invocation)

        self.assertEqual(result, expected_result)
    
    async def test_execute_should_use_functions_when_contents_call_functions(self):
        url = 'https://test.io/api'
        command_using_functions = self.build_command('Elo: {{urlfetch("' + url + '")}}!')
        invocation = CommandInvocation('test_command', ['Yuko'])

        mock_command_functions = create_autospec(AbstractCommandFunctions)
        mock_urlfetch = Mock(return_value='Diamond IV')
        mock_command_functions.get_methods.return_value = {
            'urlfetch': mock_urlfetch
        }

        command_executor = CommandExecutor(
            command_functions=mock_command_functions
        )

        expected_result = 'Elo: Diamond IV!'
        result = await command_executor.execute(command_using_functions, invocation)

        self.assertEqual(result, expected_result)
        mock_urlfetch.assert_called_with(url)
    
    async def test_execute_should_work_when_functions_and_parameters(self):
        base_url = 'https://test.io/api/'
        command_using_functions = self.build_command('Elo: {{urlfetch("' + base_url + '" + invocation.command_arguments[0])}}!')
        invocation = CommandInvocation('test_command', ['Yuko'])

        mock_command_functions = create_autospec(AbstractCommandFunctions)
        mock_urlfetch = Mock(return_value='Diamond IV')
        mock_command_functions.get_methods.return_value = {
            'urlfetch': mock_urlfetch
        }

        command_executor = CommandExecutor(
            command_functions=mock_command_functions
        )

        expected_result = 'Elo: Diamond IV!'
        result = await command_executor.execute(command_using_functions, invocation)

        self.assertEqual(result, expected_result)
        mock_urlfetch.assert_called_with('https://test.io/api/Yuko')
