from pydantic import BaseModel
from typing import List


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
