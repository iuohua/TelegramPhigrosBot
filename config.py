import json
from typing import Optional, Dict, List, Tuple

from pydantic import BaseModel

from model import User

class Config(BaseModel):
    api_id: int
    api_hash: str
    bot_token: str
    proxy: Optional[Dict|Tuple] = None
    users: List[User]
    
def get_config() -> Config:
    conf_json = json.load("config.json")
    return Config(*conf_json)