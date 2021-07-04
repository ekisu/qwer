from typing import Optional
from qwer.domain.value_objects.command_invocation import CommandInvocation


class CommandParser:
    def parse(self, message_contents: str) -> Optional[CommandInvocation]:
        if not message_contents.startswith('!'):
            return None

        command_name_with_prefix, *arguments = message_contents.split(' ')

        return CommandInvocation(
            command_name=command_name_with_prefix.strip('!'),
            command_arguments=arguments
        )
