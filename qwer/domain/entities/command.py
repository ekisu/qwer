from .registry import mapper_registry
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, Text


@mapper_registry.mapped
@dataclass
class Command:
    __tablename__ = "commands"
    __sa_dataclass_metadata_key__ = "sa"

    guild_id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String(50), primary_key=True)})
    contents: str = field(metadata={"sa": Column(Text)})
