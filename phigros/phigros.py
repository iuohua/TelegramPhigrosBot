import asyncio
from PIL import Image
from pathlib import Path
from phigrosLibrary import PhigrosLibrary

from model import PhigrosB19

class Phigros:
    def __init__(self) -> None:
        self.phigros = PhigrosLibrary()
    
    @staticmethod
    def generate_image(b19: PhigrosB19):
        ...
        
    async def get_b19_img(self, token) -> Path:
        handle = self.phigros.get_handle(token)
        b19 = self.phigros.get_b19(handle)
        
        
        
    

def get_rank(score: int, fc: int):
    if score == 1000000:
        rank = "Phi"
    else:
        if fc:
            rank = "Full Combo"
        else:
            if score < 700000:
                rank = "F"
            elif 700000 <= score <= 819999:
                rank = "C"
            elif 820000 <= score <= 879999:
                rank = "B"
            elif 880000 <= score <= 919999:
                rank = "A"
            elif 920000 <= score <= 959999:
                rank = "S"
            elif 960000 <= score <= 999999:
                rank = "V"

    return rank

def get_level(level: int) -> str:
    match level:
        case 0:
            return "EZ"
        case 1:
            return "HD"
        case 2:
            return "IN"
        case 3:
            return "AT"
        case _:
            return "Unknow"