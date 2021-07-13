from qwer.domain.entities.command import Command
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session


class CommandRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def find_command_by_guild_id_and_name(
        self, guild_id: int, name: str
    ) -> Optional[Command]:
        statement = select(Command).filter_by(
            guild_id=guild_id,
            name=name
        )

        result = self.session.execute(statement).one_or_none()
        if result is None:
            return None

        return result[Command]

    def create_command(self, command: Command):
        self.session.add(command)
        self.session.commit()

    def list_commands_by_guild_id(self, guild_id: int) -> List[Command]:
        statement = select(Command).filter_by(
            guild_id=guild_id
        )

        return [row[Command] for row in self.session.execute(statement).all()]

    def update_command(self, updated_command: Command):
        self.session.add(updated_command)
        self.session.commit()

    def delete_command(self, command: Command):
        self.session.delete(command)
        self.session.commit()
