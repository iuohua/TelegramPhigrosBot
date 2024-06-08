import ctypes
import json

from ..model import PhigrosB19

class PhigrosLibrary:
    def __init__(self) -> None:
        self.phigros = ctypes.CDLL("./libphigros-64.so")
        self.phigros.get_handle.argtypes = ctypes.c_char_p,
        self.phigros.get_handle.restype = ctypes.c_void_p
        self.higros.free_handle.argtypes = ctypes.c_void_p,
        self.phigros.get_nickname.argtypes = ctypes.c_void_p,
        self.phigros.get_nickname.restype = ctypes.c_char_p
        self.phigros.get_summary.argtypes = ctypes.c_void_p,
        self.phigros.get_summary.restype = ctypes.c_char_p
        self.phigros.get_save.argtypes = ctypes.c_void_p,
        self.phigros.get_save.restype = ctypes.c_char_p
        self.phigros.load_difficulty.argtypes = ctypes.c_void_p,
        self.phigros.get_b19.argtypes = ctypes.c_void_p,
        self.phigros.get_b19.restype = ctypes.c_char_p
        
    def get_handle(self, sessionToken: str) -> int:
        handle = self.phigros.get_handle(sessionToken)
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
        return PhigrosB19(json.loads(b19))
    
    def free_handle(self, handle: int):
        self.phigros.free_handle(handle)