from qwer.domain.entities.command import Command
from qwer.domain.value_objects.command_invocation import CommandInvocation

from qwer.services.domain.command_functions import AbstractCommandFunctions, DefaultCommandFunctions

from jinja2 import Template

class CommandExecutor:
    command_functions: AbstractCommandFunctions

    def __init__(
        self,
        command_functions: AbstractCommandFunctions = DefaultCommandFunctions()
    ):
        self.command_functions = command_functions

    def execute(self, command: Command, invocation: CommandInvocation):
        template = Template(command.contents)
        
        return template.render(
            invocation=invocation,
            **self.command_functions.get_methods()
        )
