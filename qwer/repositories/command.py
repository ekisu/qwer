from qwer.domain.entities.command import Command
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

class CommandRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def find_command_by_name(self, name: str) -> Optional[Command]:
        statement = select(Command).filter_by(name=name)

        results = self.session.execute(statement).one_or_none()
        if results is None:
            return None
        
        return results[0]
    
    def create_command(self, command: Command):
        with self.session.begin():
           self.session.add(command)
           self.session.commit()
