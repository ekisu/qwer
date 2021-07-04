from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class CommandInvocation:
    command_name: str
    command_arguments: List[str]
