from abc import ABC, abstractmethod
from typing import Any, Dict
from requests import Session


class AbstractCommandFunctions(ABC):
    @abstractmethod
    def get_methods(self) -> Dict[str, Any]:
        pass


class DefaultCommandFunctions(AbstractCommandFunctions):
    session: Session

    def __init__(self, session: Session = Session()):
        self.session = session

    def urlfetch(self, url: str) -> str:
        response = self.session.get(url)

        return response.text

    def get_methods(self) -> Dict[str, Any]:
        return {
            'urlfetch': self.urlfetch,
        }
