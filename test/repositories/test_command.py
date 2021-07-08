from qwer.domain.entities.command import Command
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from qwer.repositories.command import CommandRepository
from qwer.setup_database import setup_database
from sqlalchemy.engine import create_engine
import unittest

class TestCommandRepository(unittest.TestCase):
    session: Session
    command_repository: CommandRepository

    def setUp(self) -> None:
        engine = create_engine('sqlite:///:memory:')
        setup_database(engine)
        
        self.session = Session(engine)

        self.command_repository = CommandRepository(self.session)

    def test_create_command_should_add_record_to_database(self):
        registry_count = self.session.query(Command).count()
        self.assertEqual(registry_count, 0)

        command = Command(
            guild_id=123,
            name='test_command',
            contents='Mensagem de teste'
        )
        
        self.command_repository.create_command(command)

        registry_count = self.session.query(Command).count()
        self.assertEqual(registry_count, 1)

    def test_find_command_by_guild_id_and_name_should_be_None_when_no_commands_are_found(self):
        result = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=123,
            name="test_command"
        )

        self.assertIsNone(result)
    
    def create_sample_command(self) -> Command:
        command = Command(
            guild_id=123,
            name='test_command',
            contents='Hello, World!'
        )

        self.command_repository.create_command(command)

        return command
    
    def test_find_command_by_guild_id_and_name_should_be_None_when_guild_id_does_not_match(self):
        self.create_sample_command()

        result = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=456,
            name='test_command'
        )

        self.assertIsNone(result)

    def test_find_command_by_guild_id_and_name_should_return_Command_when_guild_id_and_name_match(self):
        command = self.create_sample_command()
        
        result = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=123,
            name='test_command'
        )

        self.assertEqual(result, command)
    
    def test_list_commands_by_guild_should_list_commands_when_they_belong_to_guild(self):
        command = self.create_sample_command()

        found_commands = self.command_repository.list_commands_by_guild_id(guild_id=123)
        self.assertEqual(1, len(found_commands))

        found_command = found_commands[0]
        self.assertEqual(command, found_command)

    def test_list_commands_by_guild_should_be_empty_when_they_belong_to_another_guild(self):
        self.create_sample_command()

        # Use a different guild id than the created command.
        found_commands = self.command_repository.list_commands_by_guild_id(guild_id=456)

        self.assertEqual(0, len(found_commands))
    
    def test_delete_command_should_be_able_to_delete(self):
        command = self.create_sample_command()

        self.command_repository.delete_command(command)

        found_command = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=command.guild_id,
            name=command.name
        )

        self.assertIsNone(found_command)
    
    def test_update_command_should_update_database_successfully(self):
        command = self.create_sample_command()

        # Try updating command name
        command.name = 'updated_test_command'
        self.command_repository.update_command(command)

        found_updated_command = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=command.guild_id,
            name='updated_test_command'
        )

        self.assertEqual(command, found_updated_command)
