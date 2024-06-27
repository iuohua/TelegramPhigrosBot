from pydantic import BaseModel
from typing import List

from telethon.extensions import markdown
from telethon import types

class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities
    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return markdown.unparse(text, entities)

class PhigrosScore(BaseModel):
    id: str
    level: int
    difficulty: float
    rks: float
    score: int
    acc: float
    fc: int
    
    
class PhigrosB19(BaseModel):
    rks: float
    phi: PhigrosScore
    best: List[PhigrosScore]
    
# class User(BaseModel):
#     user_id: int
#     token: str
