from dataclasses import dataclass
from enum import Enum

class Style(Enum):
    NS = "NS"
    AS = "AS"
    ES = "ES"
    FOUR = "FOUR"

@dataclass
class Character:
    english_name: str
    korean_class_name: str
    style: Style
    altema_url: str
    is_alter: bool = False
    alter_character_korean_name: str = None
    max_manifest: int = 0
    is_original_4star: bool = False