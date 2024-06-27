import asyncio
from PIL import Image
from pathlib import Path

from phigros.phigrosLibrary import PhigrosLibrary
from model import PhigrosB19

class Phigros:
    def __init__(self) -> None:
        self.phigros = PhigrosLibrary()
    
    @staticmethod
    def generate_image(b19: PhigrosB19):
        ...
        
    async def get_b19_img(self, token) -> Path:
        # ToDo
        handle = self.phigros.get_handle(token)
        b19 = self.phigros.get_b19(handle)
        
        
        self.phigros.free_handle(handle)
        raise NotImplementedError
        
    async def get_b19_info(self, token) -> str:
        handle = self.phigros.get_handle(token)
        b19 = self.phigros.get_b19(handle)
        rks = round(b19.rks, 2)
        if rks == -1:
            return f"Find unknown record: {b19.phi.id}"
        phi_score = b19.phi
        b19_score = b19.best
        message = f"```PhigrosB19\nYour rks: {rks}\n"
        message += "Phi: \n"  + f"    Name: {phi_score.id}\n" + f"    Score: {phi_score.score} ({round(phi_score.acc, 2)})" + f"    Difficulty: {round(phi_score.difficulty, 1)}" + f"    rks: {round(phi_score.rks, 4)}" + f"    FC: {'True' if phi_score.fc else 'False'}" + "\n"
        message += "Best19: \n"
        for i in b19_score:
            message += f"    Name: {i.id}\n" + f"    Score: {i.score} ({round(i.acc, 2)})" + f"    Difficulty: {round(i.difficulty, 1)}" + f"    rks: {round(i.rks, 4)}" + f"    FC: {'True' if i.fc else 'False'}" + "\n"
        message += "\n```"
        self.phigros.free_handle(handle)
        return message
        
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