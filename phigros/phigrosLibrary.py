import os
import ctypes
import json
from loguru import logger
from model import PhigrosB19, PhigrosScore

class PhigrosLibrary:
    def __init__(self) -> None:
        if os.name == "nt":
            self.phigros = ctypes.CDLL("./lib/phigros-64.dll")
        else:
            self.phigros = ctypes.CDLL("./lib/libphigros-64.so")
        self.phigros.get_handle.argtypes = ctypes.c_char_p,
        self.phigros.get_handle.restype = ctypes.c_void_p
        self.phigros.free_handle.argtypes = ctypes.c_void_p,
        self.phigros.get_nickname.argtypes = ctypes.c_void_p,
        self.phigros.get_nickname.restype = ctypes.c_char_p
        self.phigros.get_summary.argtypes = ctypes.c_void_p,
        self.phigros.get_summary.restype = ctypes.c_char_p
        self.phigros.get_save.argtypes = ctypes.c_void_p,
        self.phigros.get_save.restype = ctypes.c_char_p
        self.phigros.load_difficulty.argtypes = ctypes.c_void_p,
        self.phigros.get_b19.argtypes = ctypes.c_void_p,
        self.phigros.get_b19.restype = ctypes.c_char_p
        self.phigros.load_difficulty(b"./difficulty.tsv")
        
    def get_handle(self, sessionToken: str) -> int:
        handle = self.phigros.get_handle(sessionToken.encode())
        return handle
    
    def get_nickname(self, handle: int) -> str:
        nickname = self.phigros.get_nickname(handle).decode()
        return nickname
    
    def get_summary(self, handle: int) -> str:
        """
        summary: json represent as str
        """
        summary = self.phigros.get_summary(handle).decode()
        return summary
    
    def get_b19(self, handle: int) -> PhigrosB19:
        """
        Return:
            b19 data
        """
        b19 = self.phigros.get_b19(handle).decode()
        if "ERROR:std::out_of_range" in b19:
            logger.warning(f"Find unknown record, maybe because new version update: {b19}")
            return PhigrosB19(rks=-1, phi=PhigrosScore(id=b19, level=0, difficulty=-1, rks=-1, score=0, acc=0, fc=0), best=[])
        return PhigrosB19.model_validate(json.loads(b19))
    
    def free_handle(self, handle: int):
        self.phigros.free_handle(handle)