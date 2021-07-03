from typing import Optional

import discord
from sqlalchemy.sql.expression import false
import yaml
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from qwer.database.engine import engine
from qwer.domain.entities.command import Command
from qwer.repositories.command import CommandRepository

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

def find_command(message: discord.Message) -> Optional[Command]:
    message_contents: str = message.content
    command_name_with_prefix = message_contents.split()[0]

    if not command_name_with_prefix.startswith('!'):
        # Not an actual command
        return None
    
    command_name = command_name_with_prefix.strip('!')

    return command_repository.find_command_by_guild_id_and_name(
        message.guild.id,
        command_name
    )

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    handled = await try_handling_manage_command(message)
    if handled:
        return

    command = find_command(message)
    if command is not None:
        await message.channel.send(command.contents)

client.run(credentials['token'])
