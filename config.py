import json
from typing import Optional, Dict, List, Tuple

from pydantic import BaseModel

class Config(BaseModel):
    api_id: int
    api_hash: str
    bot_token: str
    proxy: Optional[Dict|Tuple] = None
    users: Dict[int, str] = {}
    owner: Optional[int] = None
    # [{id: token}, ...]
    
def get_config() -> Config:
    with open("config.json", "r", encoding="utf8") as f:
        conf_json = json.load(f)
        return Config.model_validate(conf_json)
    
def save_config(conf: Config):
    with open("config.json", "w", encoding="utf8") as f:
        f.write(conf.model_dump_json(indent=4))