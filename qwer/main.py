from typing import Optional

import discord
from sqlalchemy.sql.expression import false
import yaml
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from qwer.database.engine import engine
from qwer.domain.entities.command import Command
from qwer.repositories.command import CommandRepository
from qwer.services.domain.command_executor import CommandExecutor
from qwer.services.domain.command_parser import CommandParser

def load_credentials():
    with open('credentials.yaml') as f:
        return yaml.safe_load(f)

credentials = load_credentials()

client = discord.Client()
Session = sessionmaker(engine, future=True)

command_repository = CommandRepository(Session())

async def try_handling_manage_command(message: discord.Message) -> bool:
    message_contents: str = message.content
    is_manage_command = message_contents.startswith('!manage')

    if not is_manage_command:
        return False
    
    manage_arguments = message_contents.split(' ')
    if len(manage_arguments) < 2:
        await message.channel.send('Usage: !manage [action] [parameters]')

        return True
    
    action, *parameters = manage_arguments[1:]
    valid_actions = ['add']
    if action not in valid_actions:
        await message.channel.send(f'Invalid !manage action, valid actions are {",".join(valid_actions)}')
        
        return True
    
    if action == 'add':
        command_name = parameters[0]
        command_contents = ' '.join(parameters[1:])
        
        new_command = Command(
            guild_id=message.guild.id,
            name=command_name,
            contents=command_contents
        )

        command_repository.create_command(new_command)

        await message.channel.send(f'Command {command_name} created succesfully!')

    return True

async def try_find_command(message: discord.Message) -> None:
    command_parser = CommandParser()
    message_contents: str = message.content

    invocation = command_parser.parse(message_contents)
    if invocation is None:
        return

    command = command_repository.find_command_by_guild_id_and_name(
        message.guild.id,
        invocation.command_name
    )
    if command is None:
        return
    
    command_executor = CommandExecutor()
    response = command_executor.execute(command, invocation)

    await message.channel.send(response)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    handled = await try_handling_manage_command(message)
    if handled:
        return

    await try_find_command(message)

client.run(credentials['token'])
