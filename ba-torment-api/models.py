from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

class RaidInfo(BaseModel):
    id: str
    description: str
    is_lunatic: bool

class YoutubeLinkInfo(BaseModel):
    user_id: int
    raid_id: Optional[str] = None
    youtube_url: str
    description: str
    score: int = 0

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )