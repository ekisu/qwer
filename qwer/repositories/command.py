from qwer.domain.entities.command import Command
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

class CommandRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def find_command_by_guild_id_and_name(self, guild_id: int, name: str) -> Optional[Command]:
        statement = select(Command).filter_by(
            guild_id=guild_id,
            name=name
        )

        results = self.session.execute(statement).one_or_none()
        if results is None:
            return None
        
        return results[0]
    
    def create_command(self, command: Command):
        self.session.add(command)
        self.session.flush()
