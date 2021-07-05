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
    
    def test_find_command_by_guild_id_and_name_should_be_None_when_guild_id_does_not_match(self):
        command = Command(
            guild_id=123,
            name='test_command',
            contents='Hello, World!'
        )

        self.command_repository.create_command(command)

        result = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=456,
            name='test_command'
        )

        self.assertIsNone(result)

    def test_find_command_by_guild_id_and_name_should_return_Command_when_guild_id_and_name_match(self):
        command = Command(
            guild_id=123,
            name='test_command',
            contents='Hello, World!'
        )

        self.command_repository.create_command(command)

        result = self.command_repository.find_command_by_guild_id_and_name(
            guild_id=123,
            name='test_command'
        )

        self.assertEqual(result, command)

