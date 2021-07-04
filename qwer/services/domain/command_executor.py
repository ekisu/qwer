from qwer.domain.entities.command import Command
from qwer.domain.value_objects.command_invocation import CommandInvocation

from jinja2 import Template

class CommandExecutor:
    def execute(self, command: Command, invocation: CommandInvocation):
        template = Template(command.contents)
        
        return template.render(invocation=invocation)
